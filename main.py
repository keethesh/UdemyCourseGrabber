from functions import *

# Uncomment following lines to have an ascii_art

# ascii_art = art.text2art('''Udemy
# Course
# Grabber''', "wizard")
# print(ascii_art)
# sleep(2)
# for i in range(2):
#     print("")

udemy_url = input("Paste in your Udemy course URL: ")
course_info = get_info(udemy_url)
if course_info is None:
    exit("The course wasn't found in any of the sharing websites.")
for i in range(3):
    print("")
print("The course can be downloaded at " + course_info["link"] + ".")
print("It has been last updated in " + str(course_info["month"]) + " of " + str(course_info["year"]) + ".")
