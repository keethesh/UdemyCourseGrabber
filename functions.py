from operator import itemgetter
from threading import Thread

from selenium.common.exceptions import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from webdrivermanager import GeckoDriverManager


# from webdriver_manager.firefox import GeckoDriverManager


def get_course_name(udemy_url):
    browser.get(udemy_url)
    try:
        browser.find_element_by_css_selector(".btn-primary > span:nth-child(1)")
        course_name = browser.find_element_by_xpath(
            "//h1[contains(@class,'clp-lead__title')]").text
    except NoSuchElementException:
        raise NoSuchElementException("The provided link is broken")
    # browser.quit()
    return course_name


freecoursesite = {"search_link": "https://freecoursesite.com/?s=", "search_element": "//a[contains(text(),'",
                  "last_updated_element": "//*[contains(text(), 'Last updated')]",
                  "download_link_element": "//div[@class='audience']//p//a"}

freecourselab = {"search_link": "https://freecourselab.com/?s=",
                 "search_element": "//body[contains(@class,'bs-hide-ha bs-ll-d')]/div[contains(@class,'main-wrap "
                                   "content-main-wrap')]/div[ "
                                   "contains(@class,'content-wrap')]/main[@id='content']/div[contains(@class,"
                                   "'container layout-2-col "
                                   "layout-2-col-1 layout-right-sidebar')]/div[contains(@class,"
                                   "'row main-section')]/div[contains(@class, "
                                   "'col-sm-8 content-column')]/div[contains(@class,'listing listing-grid "
                                   "listing-grid-1 clearfix "
                                   "columns-2')]/article[1]/div[1]/div[1]/a[1]",
                 "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                 "download_link_element": "//a[contains(@class,'mb-button mb-style-flat mb-size-default "
                                          "mb-corners-default mb-text-style-default')]"}

getfreecourses = {"search_link": "https://getfreecourses.me/?s=", "search_element": "//a[contains(text(),'",
                  "last_updated_element": "//a[@class='fasc-button fasc-size-xlarge fasc-type-flat']",
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
                   "download_link_element": "//strong[contains(text(),'Download now')]"}

freecoursenet = {"search_link": "https://freecoursenet.cc/?s=", "search_element": "//a[contains(text(),'",
                 "last_updated_element": "//strong[contains(text(),'Last updated ')]",
                 "download_link_element": "//a[@class='wp-block-button__link has-background "
                                          "has-vivid-green-cyan-background-color']"}

udemy24 = {"search_link": "https://udemy24.com/?s=", "search_element": "//a[contains(text(),'",
           "last_updated_element": "//strong[contains(text(),'Last updated ')]",
           "download_link_element": "///a[contains(text(),'Download Course')]"}

sites = {"freecoursesite": freecoursesite, "freecourselab": freecourselab,
         "getfreecourses": getfreecourses, "freecourseudemy": freecourseudemy, "paidcoursesforfree": paidcoursesforfree,
         "desirecourse": desirecourse, "udemyfreecoursesdownload": udemyfreecoursesdownload,
         "tutorialsplanet": tutorialsplanet, "myfreecourses": myfreecourses, "freecoursenet": freecoursenet,
         "udemy24": udemy24}

for site in sites:
    print(site)


def set_threads(course_name):
    try:
        freecoursesite_return = Thread(target=get_info_freecoursesite, args=course_name)

    except TypeError:
        # print("The website freecoursesite.com does not have the course \"" + course_name + " available")
        pass

    try:
        freecourselab_return = Thread(target=get_info_freecourselab, args=course_name)
    except TypeError:
        # print("The website freecourselab.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        getfreecourses_return = Thread(target=get_info_getfreecourses, args=course_name)
    except TypeError:
        # print("The website getfreecourses.me does not have the course \"" + course_name + " available")
        pass

    try:
        freecourseudemy_return = Thread(target=get_info_freecourseudemy, args=course_name)
    except TypeError:
        # print("The website freecourseudemy.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        paidcoursesforfree_return = Thread(target=get_info_paidcoursesforfree, args=course_name)
    except TypeError:
        # print("The website paidcoursesforfree.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        desirecourse_return = Thread(target=get_info_desirecourse, args=course_name)
    except TypeError:
        # print("The website desirecourse.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        udemyfreecoursesdownload_return = Thread(target=get_info_udemyfreecoursesdownload, args=course_name)
    except TypeError:
        # print("The website udemyfreecoursesdownload.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        myfreecourses_return = Thread(target=get_info_myfreecourses, args=course_name)
    except TypeError:
        # print("The website myfreecourses.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        tutorialsplanet_return = Thread(target=get_info_tutorialsplanet, args=course_name)
    except TypeError:
        # print("The website tutorialsplanet.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        freecoursenet_return = Thread(target=get_info_freecoursenet, args=course_name)
    except TypeError:
        # print("The website freecoursenet.com does not have the course \"" + course_name + "\" available")
        pass


def udemy24(course_name):
    try:
        udemy24_return = Thread(target=get_info_udemy24, args=course_name)
        udemy24_date, udemy24_download = udemy24_return[0], udemy24_return[
            1]
        udemy24 = {"link": udemy24_download, "year": int(udemy24_date[1]),
                   "month": int(udemy24_date[0])}
        results.append(udemy24)
    except TypeError:
        # print("The website udemy24.com does not have the course \"" + course_name + "\" available")
        pass

    browser.quit()


def join_data(udemy_url):
    results = []
    course_name = get_course_name(udemy_url)
    all_returned = set_threads(course_name)
    freecourselab_date, freecourselab_download = freecourselab_return[0], freecourselab_return[1]
    freecourselab = {"link": freecourselab_download, "year": int(freecourselab_date[1]),
                     "month": int(freecourselab_date[0])}
    results.append(freecourselab)

    freecoursesite_date, freecoursesite_download = freecoursesite_return[0], freecoursesite_return[1]
    freecoursesite = {"link": freecoursesite_download, "year": int(freecoursesite_date[1]),
                      "month": int(freecoursesite_date[0])}
    results.append(freecoursesite)

    getfreecourses_date, getfreecourses_download = getfreecourses_return[0], getfreecourses_return[1]
    getfreecourses = {"link": getfreecourses_download, "year": int(getfreecourses_date[1]),
                      "month": int(getfreecourses_date[0])}
    results.append(getfreecourses)

    freecourseudemy_date, freecourseudemy_download = freecourseudemy_return[0], freecourseudemy_return[1]
    freecourseudemy = {"link": freecourseudemy_download, "year": int(freecourseudemy_date[1]),
                       "month": int(freecourseudemy_date[0])}
    results.append(freecourseudemy)

    paidcoursesforfree_date, paidcoursesforfree_download = paidcoursesforfree_return[0], paidcoursesforfree_return[
        1]
    paidcoursesforfree = {"link": paidcoursesforfree_download, "year": int(paidcoursesforfree_date[1]),
                          "month": int(paidcoursesforfree_date[0])}
    results.append(paidcoursesforfree)

    desirecourse_date, desirecourse_download = desirecourse_return[0], desirecourse_return[
        1]
    desirecourse = {"link": desirecourse_download, "year": int(desirecourse_date[1]),
                    "month": int(desirecourse_date[0])}
    results.append(desirecourse)

    udemyfreecoursesdownload_date, udemyfreecoursesdownload_download = udemyfreecoursesdownload_return[0], \
                                                                       udemyfreecoursesdownload_return[1]
    udemyfreecoursesdownload = {"link": udemyfreecoursesdownload_download,
                                "year": int(udemyfreecoursesdownload_date[1]),
                                "month": int(udemyfreecoursesdownload_date[0])}
    results.append(udemyfreecoursesdownload)

    myfreecourses_date, myfreecourses_download = myfreecourses_return[0], myfreecourses_return[
        1]
    myfreecourses = {"link": myfreecourses_download, "year": int(myfreecourses_date[1]),
                     "month": int(myfreecourses_date[0])}
    results.append(myfreecourses)

    tutorialsplanet_date, tutorialsplanet_download = tutorialsplanet_return[0], tutorialsplanet_return[
        1]
    tutorialsplanet = {"link": tutorialsplanet_download, "year": int(tutorialsplanet_date[1]),
                       "month": int(tutorialsplanet_date[0])}
    results.append(tutorialsplanet)

    freecoursenet_date, freecoursenet_download = freecoursenet_return[0], freecoursenet_return[
        1]
    freecoursenet = {"link": freecoursenet_download, "year": int(freecoursenet_date[1]),
                     "month": int(freecoursenet_date[0])}
    results.append(freecoursenet)

    try:
        results_sorted = sorted(results, key=itemgetter('year', 'month'), reverse=True)
    except IndexError:
        results_sorted = None
    return results_sorted


opts = Options()
# if headless == "y":
opts.add_argument("--headless")
try:
    browser = Firefox(options=opts)
except WebDriverException:
    print("Geckodriver not detected, it will now be downloaded...")
    gdd = GeckoDriverManager()
    gdd.download_and_install()
    browser = Firefox(options=opts)
