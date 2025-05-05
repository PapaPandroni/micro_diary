
#Tracking the best day so far!
def get_best_day (date, user):

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
    best_day_entries = []
    for item in best_day_entries:
        for k,v in item.items():
            if k == "entry":
                best_day_entries.append(v)
                
    return best_day_entries