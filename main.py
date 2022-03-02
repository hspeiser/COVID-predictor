import csv
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np
from collections import OrderedDict
from datetime import datetime, timedelta, date


def create_new_dir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


# Map from date to a dictionary, which itself is a map from county name to num cases
cases = OrderedDict()

# Ask the user what county they want to analyze.

countyquest = input(
    "What city would you like to see the growth of covid-19 rate for? ")
firstlt = countyquest[0]
create_new_dir(firstlt)

# Ask the user what day in the future they want us to prediction

statquest = input(
    "How many days in the future would you like to see the prediction for? ")

if statquest != "today":
    statquest = int(statquest)
elif statquest == "today":
    statquest = 0
future_days = timedelta(statquest)
day_from_now = datetime.now() + future_days

with open("counties.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for point in list(reader):
        if not point["date"] in cases:
            cases[point["date"]] = {}
        cases[point["date"]][point["county"]] = int(point["cases"])

totalcase = {}
for date in cases.keys():
    cases_on_a_given_day = cases[date]
    totalcase[date] = 0
    if countyquest != "all":
        if countyquest in cases_on_a_given_day:
            totalcase[date] = cases_on_a_given_day[countyquest]
    else:
        for county in cases_on_a_given_day.keys():
            caseday = cases_on_a_given_day[county]
            totalcase[date] += caseday

x = list(totalcase.keys())
y = list(totalcase.values())

# Go through the y values and remove any zeros you find so that Python doesn't complain.
yre = []
xre = []
for i in range(0, len(x)):
    xi = x[i]
    yi = y[i]
    if yi != 0:
        yre.append(yi)
        xre.append(xi)
y = yre
x = xre

xt = np.array(range(len(x)))
w, b = np.polyfit(xt, np.log(y), 1, w=np.sqrt(y))

first_date = datetime.strptime(x[0], "%Y-%m-%d")
stat_date = day_from_now - first_date
stat_date = stat_date.days

print(int(np.exp(b) * np.exp(w * stat_date)))

yt = np.exp(b) * np.exp(w * xt)
plt.title("Covid-19 Growth of the " + countyquest + " county.")
plt.xlabel("Date")
plt.ylabel("Number of Covid-19 cases")
'''plt.locator_params(axis='x', nbins=10)'''
plt.plot(yt, label=f"y={b:.2f}e^{w:.2f}x")
plt.scatter(x, y, label="cases", color="orange")
plt.xticks(ticks=x[::15], labels=x[::15])
plt.legend()
if countyquest != "all":
    plt.savefig(countyquest[0] + "/" + countyquest + "-county-growth")
else:
    plt.savefig("total-county-growth")
