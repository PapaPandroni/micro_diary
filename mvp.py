import datetime
import json
import os
import matplotlib.pyplot as plt

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
    
    
#this opens my file instantly, just for testing
#with open("peremil.json") as read_file:
#    peremil = json.load(read_file)

TODAY = datetime.date.today()
TODAY_STR = TODAY.isoformat()

#try/exceptblock because if its the first time opening the script last_opened wont be a datetime object
try:
    user["last_opened"] = datetime.datetime.strptime(user["last_opened"], "%Y-%m-%d").date() #converting strings json to datetime format
    delta = TODAY - user["last_opened"]
except TypeError:
    user["last_opened"] = TODAY
    #still need to define delta keyword as a timedelta object
    delta = datetime.timedelta(days=0)
    
if delta.days == 1:
#if todays opened date - last times opened date = 1 +1 streak
    user["streak"] += 1
#if its more than one, it means we skipped days. streak broken and we lose points
elif delta.days > 1:
    user["points"] -= delta.days
    user["streak"] = 0


#set last date to today and award point for opening the app.
user["last_opened"] = TODAY
user["points"] += 1 


#check for streaks. if days%7 == 0 we have a streak! +10 points and streak of 30days is 40 points
if not user["streak"]%7 and user["streak"] != 0:
    user["points"] += 10
if not user["streak"]%30 and user["streak"] !=0: 
    user["points"] += 40

#Prompt for diary entry. Ask if its encouraged behaviour (+5) or behaviour he/she wants to change (+2)
while True:
    entry = input("Enter into your diary. Type 'done' if you want to exit: ").lower()
    if entry == "done":
        break
    entry_point= input("Choose: 1. Is this behaviour encouraged by you? Or 2. Is it something you want to change?: ")
    if entry_point == "1":
        entry_point = 5
        user["points"] += 5
    elif entry_point == "2":
        entry_point = 2
        user["points"] += 2
    
    user["entries"].append({
        "date": TODAY_STR,
        "entry": entry,
        "points": entry_point 
    })

#save and update the file with new entries. must convert objects to strings in json.

user["daily_points"][TODAY_STR] = user["points"]
user["last_opened"] = TODAY_STR

with open (filename, "w") as savefile:
    json.dump(user, savefile, indent=4)
print(f"saved progress to {filename}")

#Creating a plot for showing progress:

graph = input("Do you want to see your graph of your progress? y/n: ")


if graph == "y":
    dates = [datetime.datetime.strptime(k, "%Y-%m-%d").date() for k in user["daily_points"].keys()] #converting to datetime format for matplotlib
    points = list(user["daily_points"].values()) #extracting the points

    fig, ax = plt.subplots() #creating a plot
    ax.plot(dates, points, marker="o") #plotting the datapoints and adding a visual marker to the graph

    #formatting datetime objects to exclude hours:
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    #make the plot pretty:

    fig.autofmt_xdate() #autoroates the dates (MAGIC)
    ax.set_title("Progression!") #sets the title of the plot
    ax.set_xlabel("Dates")
    ax.set_ylabel("Points")

    plt.show() #shows the plot