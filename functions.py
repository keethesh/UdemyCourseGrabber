from operator import itemgetter
from re import findall

import requests
import tldextract
from lxml import html
from lxml.etree import ParserError
from tqdm import *


def get_course_name(udemy_url):
    response = requests.get(udemy_url, headers={"User-Agent": useragent})
    if response.status_code == 404:
        raise requests.exceptions.HTTPError("404 error")
    doc = html.fromstring(response.content)
    try:
        course_name = doc.xpath("//h1[contains(@class,'clp-lead__title')]")[0].text.strip()
    except IndexError:
        course_name = None
    return course_name


def get_sites(course_name):
    course_info = []
    values = tqdm(sites.values())
    for site in values:
        ext = tldextract.extract(site.get("search_link"))
        website = ext.domain + "." + ext.suffix
        tqdm.set_description(values, desc=("Searching for course on " + website))

        response = requests.get(site.get("search_link") + course_name,
                                headers={"User-Agent": useragent}, timeout=10)
        if not response.status_code == 200:
            continue
        try:
            doc = html.fromstring(response.content)
        except ParserError:
            continue
        search_result = doc.xpath(site.get("search_element") + str(course_name) + "')]")
        if len(search_result) == 0:
            search_result = doc.xpath(site.get("search_element") + str.upper(course_name) + "')]")
            if len(search_result) == 0:
                continue
            else:
                search_result = search_result[0].get("href")
        else:
            search_result = search_result[0].get("href")
        if site.get("must_join_url"):
            search_result = "https://" + website + "/" + search_result
        response = requests.get(search_result, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                      "Chrome/80.0.3987.116 Safari/537.36"})
        doc = html.fromstring(response.content)
        last_updated = doc.xpath(site.get("last_updated_element"))[0].text
        if "custom_split" in site:
            last_updated = last_updated.split(site.get("custom_split"), 1)[1]
        else:
            last_updated = last_updated.split("Last updated ", 1)[1]
        last_updated = [last_updated.split("/", 1)[0], last_updated.split("/", 1)[1]]

        if "custom_download_link_by" in site and site.get("custom_download_link_by") == "plt":
            download_link = doc.xpath(".//a[starts-with(text(),'" + site.get("custom_download_link_by") + "')]")
            if len(download_link) == 0:
                continue
            else:
                download_link = download_link[0].get("href")
        else:
            download_link = doc.xpath(site.get("download_link_element"))
            if len(download_link) == 0:
                continue
            else:
                download_link = download_link[0].get("href")
            if "magnet" in download_link:
                download_link = findall("magnet:?xt=urn:btih:[a-zA-Z0-9]*", download_link)[0]
        course_info.append({"link": download_link, "year": int(last_updated[1]), "month": int(last_updated[0]),
                            "website": website})

    try:
        results_sorted = sorted(course_info, key=itemgetter("year", "month"), reverse=True)
    except IndexError:
        results_sorted = None
    return results_sorted


search_element_common = "//a[contains(text(),'"
last_updated_common = "//strong[contains(text(),'Last updated ')]"
freecoursesite = {"search_link": "https://freecoursesite.com/?s=", "search_element": search_element_common,
                  "last_updated_element": "//*[contains(text(), 'Last updated')]",
                  "download_link_element": "//div[@class='entry-content clearfix single-post-content']//div//div//p//a"}

freecourselab = {"search_link": "https://freecourselab.com/?s=",
                 "search_element": search_element_common,
                 "last_updated_element": last_updated_common,
                 "download_link_element": "//a[contains(@class,'mb-button mb-style-flat mb-size-default "
                                          "mb-corners-default mb-text-style-default')]"}

getfreecourses = {"search_link": "https://getfreecourses.co/?s=", "search_element": search_element_common,
                  "last_updated_element": "//div[contains(text(),'Last updated ')]",
                  "download_link_element": "//a[@class='fasc-button fasc-size-xlarge fasc-type-flat']"}

freecourseudemy = {"search_link": "https://freecourseudemy.com/?s=", "search_element": search_element_common,
                   "last_updated_element": last_updated_common,
                   "download_link_element": "//a[contains(@class,'mb-button mb-style-traditional mb-size-default "
                                            "mb-corners-default mb-text-style-heavy')]"}

paidcoursesforfree = {"search_link": "https://paidcoursesforfree.com/?s=",
                      "search_element": "//a[contains(@class,'post-title post-url')][contains(text(),'",
                      "last_updated_element": last_updated_common,
                      "download_link_element": "//a[contains(text(),'Download Now')]"}

desirecourse = {"search_link": "https://desirecourse.net/?s=", "search_element": search_element_common,
                "last_updated_element": last_updated_common,
                "download_link_element": "//a[contains(@class,'mb-button mb-style-traditional mb-size-default "
                                         "mb-corners-default mb-text-style-heavy')]"}

tutorialsplanet = {"search_link": "https://tutorialsplanet.net/?s=", "search_element": search_element_common,
                   "last_updated_element": last_updated_common,
                   "download_link_element": "//strong[contains(text(),'Download Now')]//ancestor::a"}

myfreecourses = {"search_link": "https://myfreecourses.com/?s=", "search_element": search_element_common,
                 "last_updated_element": "//span[contains(text(),'Last updated')]",
                 "download_link_element": "//body[@class='post-template-default single single-post postid-26087 "
                                          "single-format-standard has-ednbar']/div[@id='page sb-site']/div["
                                          "@id='content']/div[@id='primary']/main[@id='main']/article["
                                          "@id='post-26087']/div[@class='entry-content']/div["
                                          "@class='requirements__content']/div[@class='audience']/div["
                                          "@class='requirements__content']/div[@class='audience']/a[1]"}

freecoursenet = {"search_link": "https://freecoursenet.cc/?s=",
                 "search_element": "//a[contains(@class,'post-title post-url')][contains(text(),'",
                 "last_updated_element": last_updated_common,
                 "download_link_element": "//article//a[1]//img[1]/ancestor::a"}

udemy24 = {"search_link": "https://udemy24.com/?s=", "search_element": search_element_common,
           "last_updated_element": last_updated_common,
           "download_link_element": "//p[2]//a[1]", "must_join_url": True}

sites = {"freecoursesite": freecoursesite,
         "freecourselab": freecourselab,
         "getfreecourses": getfreecourses,
         "freecourseudemy": freecourseudemy,
         "paidcoursesforfree": paidcoursesforfree,
         "desirecourse": desirecourse,
         "tutorialsplanet": tutorialsplanet,
         "myfreecourses": myfreecourses,
         "freecoursenet": freecoursenet,
         "udemy24": udemy24}

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 " \
            "Safari/537.36 "
