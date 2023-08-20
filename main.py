import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
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

def weaknessPerMonth(results):
    weaknesses = [Weakness(row) for row in results]
    months = defaultdict(lambda: 0)
    for weakness in weaknesses:
        months[weakness.time.month] += weakness.total

    fig, ax = plt.subplots()
    sorted_keys = list(months.keys())
    sorted_keys.sort()
    sorted_amounts = [months.get(key) for key in sorted_keys]
    ax.bar(sorted_keys, sorted_amounts)
    plt.show()

def weaknessPerDayOverYear(results):
    weaknesses = [Weakness(row) for row in results]
    months = defaultdict(lambda: 0)

    week_array = [[0] * 7 for x in range(53)]

    for weakness in weaknesses:
        week = weakness.time.isocalendar().week - 1
        day = weakness.time.isocalendar().weekday - 1
        week_array[week][day] += weakness.total

    week_array = np.rot90(np.array(week_array)).round()
    fig, ax = plt.subplots()
    im = ax.imshow(week_array, cmap="RdYlGn_r")

    ax.set_yticks(np.arange(7), labels=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    ax.set_xticks(np.arange(53), labels=[ f"Week {x+1}" for x in range(53)])

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    for i in range(53):
        for j in range(7):
            text = ax.text(i, j, week_array[j, i],
                           ha="center", va="center", color="w", fontsize=5.0)


    ax.set_title("akshay weakness in 2022")
    fig.tight_layout()
    plt.show()




with sqlite3.connect("doordash.db") as connection:
    c = connection.cursor()
    results = c.execute("select STORE_NAME, DELIVERY_TIME, sum(cast(SUBTOTAL as decimal)) from doordash group by DELIVERY_TIME, STORE_NAME;")

    weaknessPerDayOverYear(results)
