import sqlite3
import matplotlib.pyplot as plt

from datetime import datetime
from collections import defaultdict

with sqlite3.connect("doordash.db") as connection:
    c = connection.cursor()
    results = c.execute("select STORE_NAME, DELIVERY_TIME, sum(cast(SUBTOTAL as decimal)) from doordash group by DELIVERY_TIME, STORE_NAME;")

    hours = defaultdict(lambda: [])

    for result in results:
        try:
            time = datetime.fromisoformat(result[1])
            hours[time.hour] = hours[time.hour] + [time]
        except:
            pass

    keys = list(hours.keys())
    keys.sort()

    for key in keys:
        print(key, len(hours.get(key)))


    fig, ax = plt.subplots()
    hour_list = keys
    counts = [len(hours.get(key)) for key in hours]
    ax.bar(hour_list, counts)
    ax.set_ylabel("moments of weakness")
    ax.set_title("akshay's moments of weakness")
    plt.show()
    
