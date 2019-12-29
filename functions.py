from operator import itemgetter

from selenium.common.exceptions import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def start_browser():
    opts = Options()
    # opts.add_argument("--headless")
    browser = Firefox(options=opts)
    return browser


def check_udemy_course(udemy_url):
    browser = start_browser()
    browser.get(udemy_url)
    try:
        browser.find_element_by_css_selector(".btn-primary > span:nth-child(1)")
        course_name = browser.find_element_by_xpath(
            "//h1[contains(@class,'clp-lead__title')]").text
    except NoSuchElementException:
        raise NoSuchElementException("The provided link is broken")
    finally:
        browser.quit()
    return course_name


def get_info_freecoursesite(course_name):
    browser = start_browser()
    browser.get("https://freecoursesite.com/?s=" + course_name)
    try:
        search_result = browser.find_element_by_xpath(
            "//a[contains(text(),'" + str(course_name) + "')]")
        search_result.click()
        last_updated = browser.find_element_by_xpath("//*[contains(text(), 'Last updated')]").text
        last_updated = last_updated.split("Last updated ", 1)[1]
        last_updated = [last_updated.split("/", 1)[0], last_updated.split("/", 1)[1]]
        download_link = browser.find_element_by_xpath("//div[@class='audience']//p//a").get_attribute("href")
        return [last_updated, download_link]
    except NoSuchElementException:
        pass
    finally:
        browser.quit()


def get_info_freecourselab(course_name):
    browser = start_browser()
    browser.get("https://freecourselab.com/?s=" + course_name)
    try:
        search_result = browser.find_element_by_xpath(
            "//body[contains(@class,'bs-hide-ha bs-ll-d')]/div[contains(@class,'main-wrap content-main-wrap')]/div["
            "contains(@class,'content-wrap')]/main[@id='content']/div[contains(@class,'container layout-2-col "
            "layout-2-col-1 layout-right-sidebar')]/div[contains(@class,'row main-section')]/div[contains(@class,"
            "'col-sm-8 content-column')]/div[contains(@class,'listing listing-grid listing-grid-1 clearfix "
            "columns-2')]/article[1]/div[1]/div[1]/a[1]")
        search_result.click()
        last_updated = browser.find_elements_by_xpath("//*[contains(text(), 'Last updated')]")
        element_to_avoid = browser.find_element_by_css_selector(
            "body.post-template-default.single.single-post.postid-3304.single-format-standard.ltr.close-rh.page-layout-2"
            "-col-right.boxed.main-menu-sticky-smart.single-prim-cat-10.single-cat-10.bs-hide-ha.bs-ll-d:nth-child(2) "
            "div.main-wrap.content-main-wrap:nth-child(1) div.content-wrap main.content-container "
            "div.container.layout-2-col.layout-2-col-1.layout-right-sidebar.post-template-1 div.row.main-section "
            "div.col-sm-8.content-column div.single-container "
            "article.post-3304.post.type-post.status-publish.format-standard.has-post-thumbnail.category-it-software.tag"
            "-hack-websites.tag-penetration-testing.tag-scratch.tag-security-experts.tag-web-applications.tag-website"
            "-hacking.single-post-content div.post-header.post-tp-1-header div.post-meta-wrap.clearfix "
            "div.post-meta.single-post-meta span.time time.post-published.updated > b:nth-child(1)")
        for element in last_updated:
            if element == element_to_avoid:
                continue
            else:
                last_updated = str(element.text)
        last_updated = last_updated.split("Last updated ", 1)[1]
        last_updated = [last_updated.split("/", 1)[0], last_updated.split("/", 1)[1]]
        download_link = browser.find_element_by_xpath(
            "//a[contains(@class,'mb-button mb-style-flat mb-size-default mb-corners-default mb-text-style-default')]").get_attribute(
            "href")
        return [last_updated, download_link]
    except NoSuchElementException:
        pass
    finally:
        browser.quit()


def get_info_getfreecourses(course_name):
    browser = start_browser()
    browser.get("https://getfreecourses.me/?s=" + course_name)
    try:
        search_result = browser.find_element_by_link_text(course_name.upper())
        search_result.click()
        last_updated = browser.find_element_by_xpath("//div[contains(text(),'Last updated')]").text
        last_updated = last_updated.split("Last updated ", 1)[1]
        last_updated = [last_updated.split("/", 1)[0], last_updated.split("/", 1)[1]]
        download_link = browser.find_element_by_xpath(
            "//a[@class='fasc-button fasc-size-xlarge fasc-type-flat']").get_attribute(
            "href")
        return [last_updated, download_link]
    except NoSuchElementException:
        pass
    finally:
        browser.quit()


def get_info(udemy_url):
    course_name = check_udemy_course(udemy_url)
    list_of_dicts = []
    try:
        getfreecourses_return = get_info_getfreecourses(course_name)
        getfreecourses_date, getfreecourses_download = getfreecourses_return[0], getfreecourses_return[1]
        getfreecourses = {"link": getfreecourses_download, "year": int(getfreecourses_date[1]),
                          "month": int(getfreecourses_date[0])}
        list_of_dicts.append(getfreecourses)
    except TypeError:
        # print("The website getfreecourses.me does not have the course \"" + course_name + " available")
        pass

    try:
        freecoursesite_return = get_info_freecoursesite(course_name)
        freecoursesite_date, freecoursesite_download = freecoursesite_return[0], freecoursesite_return[1]
        freecoursesite = {"link": freecoursesite_download, "year": int(freecoursesite_date[1]),
                          "month": int(freecoursesite_date[0])}
        list_of_dicts.append(freecoursesite)
    except TypeError:
        # print("The website freecoursesite.com does not have the course \"" + course_name + " available")
        pass

    try:
        freecourselab_return = get_info_freecourselab(course_name)
        freecourselab_date, freecourselab_download = freecourselab_return[0], freecourselab_return[1]
        freecourselab = {"link": freecourselab_download, "year": int(freecourselab_date[1]),
                         "month": int(freecourselab_date[0])}
        list_of_dicts.append(freecourselab)
    except TypeError:
        # print("The website freecourselab.com does not have the course \"" + course_name + "\" available")
        pass

    try:
        final_course = sorted(list_of_dicts, key=itemgetter('year', 'month'), reverse=True)[0]
    except IndexError:
        final_course = None
    return final_course

# print(get_info("https://www.udemy.com/course/learn-ethical-hacking-from-scratch/"))
