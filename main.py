import sqlite3
import csv
import sys
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
    ax.tick_params(axis="x", labelrotation=45)
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

    fig, ax = plt.subplots()
    plt.xticks(rotation=45, ha="right")
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

    week_array = np.rot90(np.array(week_array)).round().astype(int)
    fig, ax = plt.subplots()
    im = ax.imshow(week_array, cmap="Reds")

    ax.set_yticks(
        np.arange(7),
        labels=[
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ],
    )
    ax.set_xticks(
        np.arange(53),
        labels=[
            "",
            "Jan",
            "",
            "",
            "",
            "Feb",
            "",
            "",
            "",
            "",
            "Mar",
            "",
            "",
            "",
            "Apr",
            "",
            "",
            "",
            "",
            "May",
            "",
            "",
            "",
            "Jun",
            "",
            "",
            "",
            "Jul",
            "",
            "",
            "",
            "Aug",
            "",
            "",
            "",
            "",
            "Sep",
            "",
            "",
            "",
            "Oct",
            "",
            "",
            "",
            "",
            "Nov",
            "",
            "",
            "",
            "Dec",
            "",
            "",
            "",
        ],
    )
    # [ f"Week {x+1}" for x in range(53)])

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    for i in range(53):
        for j in range(7):
            pass
            # text = ax.text(i, j, week_array[j, i],
            #                ha="center", va="center", color="0", fontsize=12)

    ax.set_title("akshay weakness in 2022")
    fig.tight_layout()
    plt.show()

def validateRow(row):
    if len(row) != 9:
        raise Exception("Should have 9 columns in Doordash data export")

    float(row[3])

    

def importCSV(filename: str):
    CREATE_TABLE_COMMAND = """CREATE TABLE IF NOT EXISTS "doordash"(
"ITEM" TEXT, "CATEGORY" TEXT, "STORE_NAME" TEXT, "UNIT_PRICE" TEXT,
 "QUANTITY" TEXT, "SUBTOTAL" TEXT, "CREATED_AT" TEXT, "DELIVERY_TIME" TEXT,
 "DELIVERY_ADDRESS" TEXT);"""

    csvReader = csv.reader(open("yeet.csv"), delimiter=",", quotechar='"')

    filepart = filename.split(".")[0]
    conn = sqlite3.connect(f"{filepart}.db")
    c = conn.cursor()
    c.execute(CREATE_TABLE_COMMAND)

    # Skip first row.
    next(csvReader)

    for row in csvReader:
        validateRow(row)
        c.execute("insert into doordash values (?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
    conn.commit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("input csv missing")
    importCSV(sys.argv[1])
