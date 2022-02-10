import datetime
import json
import sys

eventsFile = open("events.json")
usersFile = open("users.json")

events = json.load(eventsFile)
users = json.load(usersFile)

#load users into a map from name to id
usersDict = {}
for i in users:
    usersDict[i["name"]] = i["id"]

#get ids for each user input into script
inputUserIds = set()
inputUsersEvents = []
#skipping over the script name in args
counter = 1
while counter < len(sys.argv):
    if usersDict.get(sys.argv[counter]) is None:
        raise Exception("User {} was not found in users dictionary.".format(sys.argv[counter]))
    inputUserIds.add(usersDict.get(sys.argv[counter]))
    counter += 1

#sort the events in ascending order by start time
events.sort(key=lambda x: x["start_time"])
#bootstrap with 2021-07-05 13:00:00
lastEndTime = datetime.datetime(2021, 7, 5, 13, 0, 0)
#iterate through each event, building availabilities as we go based on the events we hit since they're now in chronological order
for event in events:
    if inputUserIds.__contains__(event["user_id"]):
        #set next start time to the event's start time
        nextStartTime = datetime.datetime.strptime(event["start_time"], '%Y-%m-%dT%H:%M:%S')
        if nextStartTime.day != lastEndTime.day:
            #print the availability until the end of the last end time's day
            if lastEndTime.hour != 21:
                print(lastEndTime.strftime('%Y-%m-%dT%H:%M:%S') + "-" +
                      datetime.datetime(2021, 7, lastEndTime.day, 21, 0, 0).strftime('%Y-%m-%dT%H:%M:%S'))
            #printing a new line to separate availabilities on different days
            print()
            #reset last end time to the start of the next day
            lastEndTime = datetime.datetime(2021, 7, nextStartTime.day, 13, 0, 0)
        #handling edge case where an event starts at 13:00:00
        if nextStartTime.hour != 13 or nextStartTime.minute != 0 or nextStartTime.second != 0:
            #as long as the next event starts after the last one ends, print the time between them
            if nextStartTime > lastEndTime:
                print(lastEndTime.strftime('%Y-%m-%dT%H:%M:%S') + "-" + event["start_time"])
            elif nextStartTime < lastEndTime:
                #if the next event starts before the last one ends,
                #set the last end time to its end time if it ends after the previous event
                if datetime.datetime.strptime(event["end_time"], '%Y-%m-%dT%H:%M:%S') > lastEndTime:
                    lastEndTime = datetime.datetime.strptime(event["end_time"], '%Y-%m-%dT%H:%M:%S')
                #if the end time isn't after the previous event's, continue and don't reset last end time
                continue
        lastEndTime = datetime.datetime.strptime(event["end_time"], '%Y-%m-%dT%H:%M:%S')

#close open files
eventsFile.close()
usersFile.close()