import json
import time
import requests
import datetime as DT

now = DT.datetime.now()
target = DT.datetime.combine(DT.date.today(), DT.time(hour=8))
classes = ['English', 'Maths', 'Science', 'Digital', 'PE', 'Anc&Mod', 'RE']
scienceRoom = ['MC4', 'AD1']
mathRoom = 'WA1'
englishRoom = 'LI5'
ancmodRoom = 'MSP'
peRoom = ['OC2', 'MA7']
digitalRoom = 'DA3'
religionRoom = 'MK4'
currentDay = 1
schedule = []
day10 = False
day = 0
if now > target:
    target += DT.timedelta(days=1)
data = json
message = 'No String attached'
def pushNotification(description, title, type):
    requests.post('https://api.mynotifier.app', {
        "apiKey": '95b2edc0-a70b-4b59-9a25-10192309ea27',
        "message": title,
        "description": description,
        "type": type,
    })
def getSchedule():
    if day < 5: 
        day10 = False
        data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Bundaberg&units=metric&APPID=6be1c15b5cabc76d52b63dd7c23a3245")
        if currentDay == 1 and day == 0:
            schedule = [classes[2], scienceRoom[0], classes[1], mathRoom, classes[5], ancmodRoom, classes[0], englishRoom]
        elif currentDay == 2 and day == 1:
            schedule = [classes[3], digitalRoom, classes[6], religionRoom, classes[4], peRoom[0], classes[2], scienceRoom[1]]
        elif currentDay == 3 and day == 2:
            schedule = [classes[0], englishRoom, classes[5], ancmodRoom, classes[4], peRoom[1], classes[3], digitalRoom]
        elif currentDay == 5 and day == 4:
            schedule = [classes[6], religionRoom, classes[3], digitalRoom, classes[2], scienceRoom[0], classes[1], mathRoom]
        elif currentDay == 4 and day == 3:
            schedule = [classes[1], mathRoom, classes[2], scienceRoom[1], classes[5], ancmodRoom, classes[0], englishRoom]
        elif currentDay == 6 and day == 0:
            schedule = [classes[5], ancmodRoom, classes[0], englishRoom, classes[3], digitalRoom, classes[4], peRoom[0]]
        elif currentDay == 7 and day == 1:
            schedule = [classes[2], scienceRoom[1], classes[1], mathRoom, classes[0], englishRoom, classes[5], ancmodRoom]
        elif currentDay == 8 and day == 2:
            schedule = [classes[3], digitalRoom, classes[6], religionRoom, classes[1], mathRoom, classes[2], scienceRoom[0]]
        elif currentDay == 9 and day == 3:
            schedule = [classes[0], englishRoom, classes[5], ancmodRoom, classes[1], mathRoom, classes[3], digitalRoom]
        elif currentDay == 10 and day == 4:
            day10 = True 
        elif day < 4:
          print("its saturday or sunday")
        else:
            pushNotification("PROCESS HAS ENCOUNTERED AN ERROR, FIX ASAP", "ERROR", "error")
            print(currentDay, day, schedule, now, target, day10)
            exit()
        if day10 is True:
            currentDay = 1
            message = f"Good Morning! \nToday is Day 10, so check SIA for your schedule. \nThe current temperature is {data.json().get('main')['temp']}°C"
        else:
            currentDay += 1
            message = f"Good Morning! \nHeres your schedule for today! \n{schedule[0]} in {schedule[1]}, {schedule[2]} in {schedule[3]}, {schedule[4]} in {schedule[5]} and finally {schedule[6]} in {schedule[7]}\nThe current temperature is {data.json().get('main')['temp']}°C"
        pushNotification(message, "Daily Notification!", "success")
while True:
    time.sleep(2)
    now = DT.datetime.now()
    day = DT.datetime.today().weekday()
    if target < now:
        target += DT.timedelta(days=1)
        getSchedule()
