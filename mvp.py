import datetime
import json
import os

from functions import *

from constants import TODAY, TODAY_STR

#start the program. Check for save file. otherwise create a save file.
savefile = [file for file in os.listdir() if file.endswith(".json") and file != "template.json"]


if not savefile:
    with open("template.json") as template:
        user = json.load(template)
    print("created a new user")
    filename = "user.json"
    
else:
    filename = savefile[0]
    with open(filename) as existing_user:
        user = json.load(existing_user)
    print(f"opened existing user save file called: {filename}")

#check for streaks must be done before changing last opened.

check_streaks(user)

#set last date to today and award point for opening the app.
user["last_opened"] = TODAY
user["points"] += 1 

#Prompt for diary entry. Ask if its encouraged behaviour (+5) or behaviour he/she wants to change (+2)

microblog_entries(user)


#save and update the file with new entries. must convert objects to strings in json.

user["daily_points"][TODAY_STR] = user["points"]
user["last_opened"] = TODAY_STR

with open (filename, "w") as savefile:
    json.dump(user, savefile, indent=4)
print(f"saved progress to {filename}")

#get the best day so far:

best_day=get_best_day(user)

print(f"Your best day pointwise is: {best_day}")
#get the entries from the best day so far

best_entries = get_best_day_entries(best_day, user)

print(f"On this day you wrote:")

for entry in best_entries:
    print(entry)
    

#Creating a plot for showing progress:

print_graph(user)