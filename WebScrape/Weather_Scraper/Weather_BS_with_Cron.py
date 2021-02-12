import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date
import datetime
import schedule
import time

now = 0
print()


def job():
    pass
    print("running scraper")
    page = requests.get(
        'https://forecast.weather.gov/MapClick.php?lat=33.95469700000007&lon=-83.39643609999996#.X3Pvvi9h1QI')
    soup = BeautifulSoup(page.content, 'html.parser')
    week = soup.find(id='seven-day-forecast-body')
    items = week.find_all(class_='tombstone-container')
    temp = items[0].find(class_='temp').get_text()
    short_discription = items[0].find(class_='short-desc').get_text()
    Day = items[0].find(class_='period-name').get_text()
    period_name = [item.find(class_='period-name').get_text() for item in items]
    Daay = []
    night = " Night"
    w = 1
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    for i in range(1, 8, 2):
        Daay.append(d2)
        x = d2 + night
        Daay.append(x)
        d2 = datetime.datetime.today() + datetime.timedelta(days=w)
        d2 = d2.strftime("%B %d, %Y")
        w = w + 1
    Daay.append(d2)
    print(Daay)
    temprature = [item.find(class_='temp').get_text() for item in items]
    short_discriptions = [item.find(class_='short-desc').get_text() for item in items]
    weather_stuff = pd.DataFrame(
        {'Period': Daay,
         'Description': short_discription,
         'Temprature': temprature
         }
    )
    print(weather_stuff)
    print("Now exporting to CSV")
    weather_stuff.to_csv('Weather_Data.csv', index=False)
    print("exported")


schedule.every().wednesday.at("08:00").do(job)

while True:
    print("will run in ",((now/604800)*100)," seconds left ",(604800-now))
    schedule.run_pending()
    time.sleep(10)  # wait one minute
    now = now + 1
