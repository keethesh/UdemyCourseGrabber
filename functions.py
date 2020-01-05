from operator import itemgetter

import tldextract
from selenium.common.exceptions import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.firefox.options import Options
from tqdm import *
from webdrivermanager import GeckoDriverManager


def start_browser():
    opts = Options()
    # if headless == "y":
    opts.add_argument("--headless")
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    try:
        driver = Firefox(firefox_profile=firefox_profile, options=opts)
    except WebDriverException:
        print("Geckodriver not detected, it will now be downloaded...")
        gdd = GeckoDriverManager()
        gdd.download_and_install()
        driver = Firefox(firefox_profile=firefox_profile, options=opts)
    return driver


def get_course_name(udemy_url):
    browser.get(udemy_url)
    try:
        browser.find_element_by_xpath("//span[contains(text(),'Add to cart')]")
        course_name = browser.find_element_by_xpath(
            "//h1[contains(@class,'clp-lead__title')]").text
    except NoSuchElementException:
        raise NoSuchElementException("The provided link is broken")
    return course_name


def get_sites(course_name):
    course_info = []
    values = tqdm(sites.values())
    for site in values:
        ext = tldextract.extract(site.get("search_link"))
        website = ext.domain + "." + ext.suffix
        tqdm.set_description(values, desc=("Searching for course on " + website))
        successful = False

        while not successful:
            browser.get(site.get("search_link") + course_name)

            try:
                search_result = browser.find_element_by_xpath(
                    site.get("search_element") + str(course_name) + "')]")

            except NoSuchElementException:
                try:
                    search_result = browser.find_element_by_xpath(
                        site.get("search_element") + str(course_name).upper() + "')]")
                except NoSuchElementException:
                    successful = True
                    continue
            try:
                search_result.click()
                last_updated = browser.find_element_by_xpath(site.get("last_updated_element")).text

                if "custom_split" in site:
                    last_updated = last_updated.split(site.get("custom_split"), 1)[1]
                else:
                    last_updated = last_updated.split("Last updated ", 1)[1]
                last_updated = [last_updated.split("/", 1)[0], last_updated.split("/", 1)[1]]

                if "custom_download_link_by" in site and site.get("custom_download_link_by") == "plt":
                    download_link = browser.find_element_by_partial_link_text(
                        site.get("download_link_element")).get_attribute("href")
                else:
                    download_link = browser.find_element_by_xpath(site.get("download_link_element")).get_attribute(
                        "href")
                course_info.append({"link": download_link, "year": int(last_updated[1]), "month": int(last_updated[0]),
                                    "website": website})
                successful = True

            except ElementClickInterceptedException:
                successful = False

            except NoSuchElementException:
                successful = True
                continue

    browser.quit()

    try:
        results_sorted = sorted(course_info, key=itemgetter("year", "month"), reverse=True)
    except IndexError:
        results_sorted = None
    return results_sorted


freecoursesite = {"search_link": "https://freecoursesite.com/?s=", "search_element": "//a[contains(text(),'",
                  "last_updated_element": "//*[contains(text(), 'Last updated')]",
                  "download_link_element": "//div[@class='audience']//p//a"}

freecourselab = {"search_link": "https://freecourselab.com/?s=",
                 "search_element": "//a[contains(text(),'",
                 "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                 "download_link_element": "//a[contains(@class,'mb-button mb-style-flat mb-size-default "
                                          "mb-corners-default mb-text-style-default')]"}

getfreecourses = {"search_link": "https://getfreecourses.me/?s=", "search_element": "//a[contains(text(),'",
                  "last_updated_element": "//div[contains(text(),'Last updated ')]",
                  "download_link_element": "//a[@class='fasc-button fasc-size-xlarge fasc-type-flat']"}

freecourseudemy = {"search_link": "https://freecourseudemy.com/?s=", "search_element": "//a[contains(text(),'",
                   "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                   "download_link_element": "//a[contains(@class,'mb-button mb-style-traditional mb-size-default "
                                            "mb-corners-default mb-text-style-heavy')]"}

paidcoursesforfree = {"search_link": "https://paidcoursesforfree.com/?s=", "search_element": "//a[contains(text(),'",
                      "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                      "download_link_element": "Udemy – ", "custom_download_link_by": "plt"}

desirecourse = {"search_link": "https://desirecourse.net/?s=", "search_element": "//a[contains(text(),'",
                "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                "download_link_element": "//a[contains(@class,'mb-button mb-style-traditional mb-size-default "
                                         "mb-corners-default "
                                         "mb-text-style-heavy')]"}

udemyfreecoursesdownload = {"search_link": "https://udemyfreecoursesdownload.com/?s=",
                            "search_element": "//a[contains(text(),'",
                            "last_updated_element": "//div[contains(text(),'Final up to date')]",
                            "download_link_element": "//a[@class='fasc-button fasc-size-xlarge fasc-type-flat']",
                            "custom_split": "Final up to date "}

myfreecourses = {"search_link": "https://myfreecourses.com/?s=", "search_element": "//a[contains(text(),'",
                 "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                 "download_link_element": "//body[@class='post-template-default single single-post postid-26087 "
                                          "single-format-standard has-ednbar']/div[@id='page sb-site']/div["
                                          "@id='content']/div[@id='primary']/main[@id='main']/article["
                                          "@id='post-26087']/div[@class='entry-content']/div["
                                          "@class='requirements__content']/div[@class='audience']/div["
                                          "@class='requirements__content']/div[@class='audience']/a[1]"}

tutorialsplanet = {"search_link": "https://tutorialsplanet.net/?s=", "search_element": "//a[contains(text(),'",
                   "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                   "download_link_element": "//div[contains(@class,'audience')]//p//a"}

freecoursenet = {"search_link": "https://freecoursenet.cc/?s=", "search_element": "//a[contains(text(),'",
                 "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                 "download_link_element": "//strong[contains(text(),'Download now')]"}

udemy24 = {"search_link": "https://udemy24.com/?s=", "search_element": "//a[contains(text(),'",
           "last_updated_element": "//strong[contains(text(),'Last updated ')]",
           "download_link_element": "///a[contains(text(),'Download Course')]"}

sites = {"freecoursesite": freecoursesite,
         "freecourselab": freecourselab,
         "getfreecourses": getfreecourses,
         "freecourseudemy": freecourseudemy,
         "paidcoursesforfree": paidcoursesforfree,
         "desirecourse": desirecourse,
         "udemyfreecoursesdownload": udemyfreecoursesdownload,
         "tutorialsplanet": tutorialsplanet,
         "myfreecourses": myfreecourses,
         "freecoursenet": freecoursenet,
         "udemy24": udemy24}

browser = start_browser()
