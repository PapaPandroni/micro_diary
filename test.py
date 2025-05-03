import os
import json

import matplotlib.pyplot as plt
import datetime

        
#Tracking the best day so far!

with open("peremil.json") as file:
    user = json.load(file)

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

print(best_date)        

# find the entries of the best day

best_day_entries = list(filter(lambda entry: entry["date"] == best_date, user["entries"]))

for item in best_day_entries:
    for k,v in item.items():
        if k == "entry":
            print(f"{v}")