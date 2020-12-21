import asyncio
import sys
from operator import itemgetter
from re import compile

import aiohttp
import validators
from lxml import html
from tqdm.asyncio import tqdm


class Error(Exception):
    pass


class NoCourseInfoException(Error):
    def __init__(self, message="No information about the course has been given to the Scraper class"):
        self.message = message
        super().__init__(self.message)


class Scraper:
    def __init__(self, course):
        if course is None:
            raise NoCourseInfoException

        self.__useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                           'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                           'Chrome/86.0.4240.75 Safari/537.36'
        self.__common_updated_xpath = "//strong[contains(text(),'Last updated ')]"

        self.__regex = compile("magnet:\?xt=urn:btih:[a-zA-Z0-9]*")

        if sys.platform == "win32":
            self.loop = asyncio.ProactorEventLoop()
        else:
            self.loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(self.loop)

        if validators.url(course):
            self._course_url = course
            self.course_name = self.loop.run_until_complete(self.get_course_name())
        else:
            print("The value entered is not a link, taking it as the course name.\n")
            self.course_name = course

        self.__mod_name = self.course_name.replace("-", "")
        self.__scraping_funcs = [self.__freecoursesite,
                                 self.__getfreecourses,
                                 self.__freecourseudemy,
                                 self.__paidcoursesforfree,
                                 self.__desirecourse,
                                 self.__tutorialsplanet,
                                 self.__myfreecourses,
                                 self.__udemy24,
                                 self.__freeallcourse,
                                 self.__freecoursesdownload,
                                 self.__freetutorialsudemy]

    async def get_course_name(self):
        async with aiohttp.ClientSession(headers={"User-Agent": self.__useragent}, timeout=aiohttp.ClientTimeout(10)) \
                as session:
            async with session.get(self._course_url) as response:
                response = await response.read()
        doc = html.fromstring(response)
        try:
            course_name = doc.xpath("//h1[contains(@class,'clp-lead__title')]")[0].text.strip()
        except IndexError:
            course_name = None
        return course_name

    def search_course(self):
        results = self.loop.run_until_complete(self.__search_course())
        if results:
            results = sorted(results, key=itemgetter("year", "month"), reverse=True)
        return results

    async def __search_course(self):
        results = []
        async with aiohttp.ClientSession(headers={"User-Agent": self.__useragent}, timeout=aiohttp.ClientTimeout(10)) \
                as session:
            tasks = tuple(func(session) for func in self.__scraping_funcs)
            for func in tqdm.as_completed(tasks, loop=self.loop):
                result = await func
                if result:
                    last_updated = [int(i) for i in result['last_updated'].split('Last updated ')[1].split('/')]
                    if len(str(last_updated[0])) < len(str(last_updated[1])):
                        last_updated = last_updated[::-1]
                    result['year'], result['month'] = last_updated
                    results.append(result)

        return results

    async def __freecoursesite(self, session):
        async with session.get(f'https://freecoursesite.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)
            download_link = doc.xpath("//strong[starts-with(text(),'Download Now')]/ancestor::a")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'freecoursesite.com'}

    async def __getfreecourses(self, session):
        async with session.get(f'https://getfreecourses.co/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[starts-with(text(),'DOWNLOAD TUTORIAL')]")[0].get('href')
            last_updated = doc.xpath("//div[starts-with(text(),'Last updated ')]")[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'getfreecourses.co'}

    async def __freecourseudemy(self, session):
        async with session.get(f'https://freecourseudemy.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[starts-with(text(),'DOWNLOAD COURSE')]")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'freecourseudemy.com'}

    async def __paidcoursesforfree(self, session):
        async with session.get(f'https://paidcoursesforfree.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)
            download_link = doc.xpath("//h1/a[@href]")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text

        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'paidcoursesforfree.com'}

    async def __desirecourse(self, session):
        async with session.get(f'https://desirecourse.net/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[contains(text(),'DOWNLOAD COURSE')]")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'desirecourse.net'}

    async def __tutorialsplanet(self, session):
        async with session.get(f'https://tutorialsplanet.net/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//div[@data-purpose='course-audience']/p/a")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'tutorialsplanet.net'}

    async def __myfreecourses(self, session):
        async with session.get(f'https://myfreecourses.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[@id='download']")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'myfreecourses.com'}

    async def __udemy24(self, session):
        async with session.get(f'https://udemy24.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//strong[contains(text(),'Download Course')]//ancestor::a")[0].get('href')
            last_updated = doc.xpath("//strong[contains(text(),'Last updated : ')]")[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'udemy24.com'}

    async def __freeallcourse(self, session):
        async with session.get(f'https://freeallcourse.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[contains(text(),'Download Course')]")[0].get('href')
            last_updated = doc.xpath("//strong/br")[0].tail
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'freeallcourse.com'}

    async def __freecoursesdownload(self, session):
        async with session.get(f'https://freecoursesdownload.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[contains(text(),'DOWNLOAD COURSE')]")[0].get('href')
            last_updated = doc.xpath(self.__common_updated_xpath)[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'freecoursesdownload.com'}

    async def __freetutorialsudemy(self, session):
        async with session.get(f'https://freetutorialsudemy.com/?s={self.__mod_name}') as response:
            response = await response.read()
        doc = html.fromstring(response)
        search_results = doc.xpath(f"//a[contains(text(),'{self.__mod_name}')]")
        if not search_results:
            return
        try:
            async with session.get(search_results[0].get("href")) as response:
                response = await response.read()
            doc = html.fromstring(response)

            download_link = doc.xpath("//a[contains(text(),'Download link')]")[0].get('href')
            last_updated = doc.xpath("//strong/text()[contains(.,'Last updated ')]")[0].text
        except (IndexError, KeyError):
            return

        magnet_links = self.__regex.findall(download_link)
        if magnet_links:
            download_link = magnet_links[0]
        return {"link": download_link, "last_updated": last_updated, "website": 'freetutorialsudemy.com'}
