import sqlite3
import matplotlib.pyplot as plt

from datetime import datetime
from collections import defaultdict

def weakness_by_hours(hours):
    keys = list(hours.keys())
    keys.sort()

    for key in keys:
        print(key, len(hours.get(key)))


    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelrotation=45)
    hour_list = keys
    counts = [len(hours.get(key)) for key in hours]
    ax.bar(hour_list, counts)
    ax.set_ylabel("moments of weakness")
    ax.set_title("akshay's moments of weakness")
    plt.show()

class Weakness:
    def __init__(self, row):
        self.name = row[0]
        try: 
            self.time = datetime.fromisoformat(row[1])
        except:
            self.time = datetime.today()
        self.total = row[2]

def weaknessInAnHour(results):
    weaknesses = [Weakness(row) for row in results]
    restaurants = defaultdict(lambda: 0)

    for weakness in weaknesses:
        if weakness.time.hour == 0:
            restaurants[weakness.name] += 1

    print(restaurants)

    fig, ax = plt.subplots()
    plt.xticks(rotation=45, ha='right')
    ax.bar(restaurants.keys(), restaurants.values())
    plt.show()

    

with sqlite3.connect("doordash.db") as connection:
    c = connection.cursor()
    results = c.execute("select STORE_NAME, DELIVERY_TIME, sum(cast(SUBTOTAL as decimal)) from doordash group by DELIVERY_TIME, STORE_NAME;")

    weaknessInAnHour(results)

 


