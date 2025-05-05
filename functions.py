from constants import TODAY, TODAY_STR
import matplotlib.pyplot as plt
import datetime

#Tracking the best day so far!
def get_best_day (user):

    #find the best day:
    highest_delta = 0
    last_value = 0
    best_date = None
    for date in sorted(user["daily_points"]):
        delta = (user["daily_points"][date] - last_value)
        if delta > highest_delta:
            best_date = date
            highest_delta = delta
        last_value = user["daily_points"][date]

    return best_date      


    # find the entries of the best day
def get_best_day_entries(best_date, user):
    best_day_entries = list(filter(lambda entry: entry["date"] == best_date, user["entries"]))
    best_day_entries_list = []
    for item in best_day_entries:
        for k,v in item.items():
            if k == "entry":
                best_day_entries_list.append(v)
             
    return best_day_entries_list
    

def check_streaks(user):
    
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
    
    #check for long streaks. if days%7 == 0 we have a streak! +10 points and streak of 30days is 40 points
    if not user["streak"]%7 and user["streak"] != 0:
        user["points"] += 10
    if not user["streak"]%30 and user["streak"] !=0: 
        user["points"] += 40


def microblog_entries(user):
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
        
def print_graph(user):
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