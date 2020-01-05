import time
from re import findall

import pyperclip

from functions import *

udemy_url = input("Paste in your Udemy course URL: ")
print("")

course_name = get_course_name(udemy_url)
course_info = get_sites(course_name)

if len(course_info) == 0:
    exit("The course wasn't found in any of the sharing websites.")
for i in range(3):
    print("")
download_link = course_info[0].get("link")

if "magnet" in download_link:
    download_link = findall("magnet:?xt=urn:btih:[a-zA-Z0-9]*", download_link)[0]
print("The Udemy course \"" + course_name + "\" can be downloaded at " + download_link)
print("It has last been updated on " + str(course_info[0]["month"]) + "/" + str(course_info[0]["year"]) +
      ", and was fetched from " + str(course_info[0]["website"]))
print("")

copy_to_clipboard = input("Do you want me to copy the link to your clipboard? (Y/n): ").upper()
if copy_to_clipboard == "Y" or copy_to_clipboard != "N":
    pyperclip.copy(download_link)
    print("The link has successfully been copied to clipboard.")

if len(course_info) > 1:
    see_all = input("Do you want to see the other links as well? (y/N): ").lower()
    if not see_all == ("y" or "n"):
        see_all = "n"
    if see_all == "y":
        for i in range(1, len(course_info)):
            print("")
            print("Last update: " + str(course_info[i]["month"]) + "/" + str(course_info[i]["year"]))
            print("Download link: " + str(course_info[i]["link"]))
            print("From website: " + str(course_info[i]["website"]))
            print("")

time.sleep(0.5)
exit("My work here is done. Script execution finished.")
