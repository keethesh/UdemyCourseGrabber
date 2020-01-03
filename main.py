import time
from re import findall

import pyperclip

udemy_url = input("Paste in your Udemy course URL: ")
print("")
print("Search starting...")
# headless = input("Do you want to run the browser in headless mode? (Y/n): ").lower()
# if not headless == ("y" or "n"):
#     headless = "y"
course_name = get_course_name(udemy_url)
course_info = get_sites(course_name)
if len(course_info) == 0:
    exit("The course wasn't found in any of the sharing websites.")
for i in range(3):
    print("")
download_link = course_info[0].get("link")
try:
    if "magnet" in download_link:
        download_link = findall("magnet:?xt=urn:btih:[a-zA-Z0-9]*", download_link)
except TypeError:
    pass
print("The Udemy course \"" + course_name + "\" can be downloaded at " + download_link)
print("It has last been updated on " + str(course_info[0]["month"]) + "/" + str(course_info[0]["year"]) + ".")
copy_to_clipboard = input("Do you want me to copy the link to your clipboard? (Y/n): ").upper()
if not copy_to_clipboard == "Y" or copy_to_clipboard == "N":
    copy_to_clipboard = "Y"
if copy_to_clipboard == "Y":
    pyperclip.copy(download_link)
    print("")
    print("The link has successfully been copied to clipboard.")

if len(course_info) > 1:
    see_all = input("Do you want to see the other links as well? (y/N): ").lower()
    if not see_all == ("y" or "n"):
        see_all = "n"
    if see_all == "y":
        for i in range(1, len(course_info)):
            print("Last update: " + str(course_info[i]["month"]) + "/" + str(course_info[i]["year"]))
            print("Download link: " + str(course_info[i]["link"]))
            print("")

time.sleep(1)
exit("My work here is done. Script execution finished.")
