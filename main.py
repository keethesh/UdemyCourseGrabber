import argparse
import csv
import sys
import time

import pyperclip

import scrapers


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def write_to_file(data_dict, filename):
    with open(filename, mode='a+', encoding="UTF-8", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_file.seek(0, 2)
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(data_dict)


def command_line(udemy_url, copy_to_clipboard=False, filename="output.csv"):
    scraper = scrapers.Scraper(udemy_url)
    original_course_name = scraper.course_name

    course_info = scraper.search_course()

    if not course_info:
        exit("The course wasn't found on any of the websites.")

    download_link = course_info[0].get("link")
    last_updated = str(course_info[0]["month"]) + "/" + str(course_info[0]["year"])
    from_website = course_info[0].get("website")
    print("Download link: " + download_link)
    print("Last updated: " + last_updated)
    print("Fetched from " + from_website)
    if copy_to_clipboard:
        pyperclip.copy(download_link)

    if not filename == "":
        for info in course_info:
            download_link = info.get("link")
            last_updated = str(info["month"]) + "/" + str(info["year"])
            from_website = info.get("website")
            data = {"Course name": original_course_name, "Last updated": last_updated, "Download Link": download_link,
                    "Provider": from_website}
            write_to_file(data, filename)


def interactive():
    print("\n")
    udemy_url = input("Paste in your Udemy course URL, or the course name: ").strip()
    scraper = scrapers.Scraper(udemy_url)

    original_course_name = scraper.course_name
    course_info = scraper.search_course()

    if len(course_info) == 0:
        exit("The course wasn't found in any of the sharing websites.")
    print("\n\n\n")
    download_link = course_info[0].get("link")

    print("The Udemy course \"" + original_course_name + "\" can be downloaded at " + download_link)
    print("It has last been updated on " + str(course_info[0]["month"]) + "/" + str(course_info[0]["year"]) +
          ", and was fetched from " + str(course_info[0]["website"]) + "\n")

    copy_to_clipboard = input("Do you want me to copy the link to your clipboard? (Y/n): ")
    if str2bool(copy_to_clipboard):
        pyperclip.copy(download_link)
        print("The link has successfully been copied to the clipboard.")

    if len(course_info) > 1:
        see_all = input("Do you want to see the other links as well? (y/N): ")
        if str2bool(see_all):
            print('\n')
            for i in range(1, len(course_info)):
                print(f'Last update: {str(course_info[i]["month"])}/{str(course_info[i]["year"])}')
                download_link = str(course_info[i]["link"])
                print(f'Download link: {download_link}')
                print(f'From {str(course_info[i]["website"])}\n')


fieldnames = ["Course name", "Last updated", "Download Link", "Provider"]
if len(sys.argv) == 1:
    interactive()
else:
    parser = argparse.ArgumentParser(description='Script that searches for "ripped" Udemy courses')
    parser.add_argument("course")
    parser.add_argument("-c", action='store_true', default=True,
                        help="Add this flag to copy the download link to clipboard")
    parser.add_argument("-o", type=str, nargs='?', const=True, default="output.csv",
                        help="Stores the outputs to the specified CSV file. Pass argument \"plsno\" to disable "
                             "writing to file.")

    args = parser.parse_args()
    course = args.course
    clipboard = args.c
    output_file = args.o

    if output_file == "plsno":
        output_file = ""
    command_line(course, clipboard, output_file)
time.sleep(0.5)
exit("My work here is done. Script execution finished.")
