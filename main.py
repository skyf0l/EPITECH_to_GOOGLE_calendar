#!/usr/bin/env python3

from google_calendar import service

from sys import argv
from datetime import datetime, timedelta
import os
import requests
import json

# config

EPITECH_AUTOLOGIN = os.getenv("EPITECH_AUTOLOGIN")
if EPITECH_AUTOLOGIN is None:
    print("EPITECH_AUTOLOGIN not in env")
    exit(1)

config = json.load(open("config.json"))
CALENDAR_ID_EVENTS = config['calendarID_events']
CALENDAR_ID_TIMELINE = config['calendarID_timeline']


# format: start/end => datetime
# get_epitech_events() => all after one month before today
# get_epitech_events(start) => all after start
# get_epitech_events(end) => all in one month before end and end

def get_epitech_events(start=None, end=None):
    url = f'https://intra.epitech.eu/{EPITECH_AUTOLOGIN}/planning/load?format=json'
    if start is not None:
        url += '&start=' + start.strftime('%Y-%m-%d')
    if end is not None:
        url += '&end=' + end.strftime('%Y-%m-%d')
    return requests.get(url).json()


# same as get_epitech_events but keep only registered events
# /!\ english delivery not marked as registered

def get_my_epitech_events(start=None, end=None):
    events = get_epitech_events(start=start, end=end)
    events_registered = []
    for event in events:
        if 'event_registered' in event and event['event_registered'] is not False:
            events_registered.append(event)
    return events_registered


# format: start/end => datetime
# get_my_epitech_activities() => current week
# get_my_epitech_activities(start) => all after start included
# get_my_epitech_activities(end) => all in one month before end and end

def get_my_epitech_activities(start=None, end=None):
    if start is None and end is None:
        current_date = datetime.today()
        start = current_date - timedelta(days=current_date.weekday())
        end = start + timedelta(weeks=1)
    elif start is None:
        start = end - timedelta(days=31)
    elif end is None:
        end = start + timedelta(days=365)

    url = f'https://intra.epitech.eu/{EPITECH_AUTOLOGIN}/module/board/?format=json&start={start.strftime("%Y-%m-%d")}&end={end.strftime("%Y-%m-%d")}'
    return requests.get(url).json()


# same as get_my_epitech_activities but keep only registered projects

def get_my_epitech_registered_projects(start=None, end=None):
    activities = get_my_epitech_activities(start, end)
    projets = []

    for activity in activities:
        if 'registered' in activity and activity['registered'] == 1:
            if 'type_acti_code' in activity and activity['type_acti_code'] == 'proj':
                projets.append(activity)

    return projets


# return right (start, end) of event

def get_epitech_event_date(event):
    if 'rdv_group_registered' in event and event['rdv_group_registered'] is not None:
        return event['rdv_group_registered'].split('|')
    elif 'rdv_indiv_registered' in event and event['rdv_indiv_registered'] is not None:
        return event['rdv_indiv_registered'].split('|')
    return event['start'], event['end']


# add event to google calendar

def add_google_calendar_event(calendarID, event):
    event_start, event_end = get_epitech_event_date(event)
    event = {
        "summary": event['codemodule'] + ' - ' + event['acti_title'],
        # "location": "location",
        # "description": "description",
        "start": {
            "dateTime": event_start.replace(' ', 'T'),
            "timeZone": "Europe/Paris"
        },
        "end": {
            "dateTime": event_end.replace(' ', 'T'),
            "timeZone": "Europe/Paris"
        },
    }
    service.events().insert(calendarId=calendarID, body=event).execute()


# add project to google calendar

def add_google_calendar_project(calendarID, project):
    event = {
        "summary": project['codemodule'] + ' - ' + project['acti_title'],
        # "location": "location",
        # "description": "description",
        "start": {
            "dateTime": project['begin_acti'].replace(' ', 'T'),
            "timeZone": "Europe/Paris"
        },
        "end": {
            "dateTime": project['end_acti'].replace(' ', 'T'),
            "timeZone": "Europe/Paris"
        },
    }
    service.events().insert(calendarId=calendarID, body=event).execute()


# update callendar from monday of current week
if len(argv) == 2:
    current_date = datetime.strptime(argv[1], '%Y-%m-%d')
else:
    current_date = datetime.today()
monday_of_current_week = current_date - timedelta(days=current_date.weekday())

my_events = get_my_epitech_events(start=monday_of_current_week)

print(f'{len(my_events)} events registered:')
for event in my_events:
    event_start, event_end = get_epitech_event_date(event)
    print(event_start + ' - ' + event_end + ' -> ' + event['acti_title'])
    add_google_calendar_event(CALENDAR_ID_EVENTS, event)

print()

my_projects = get_my_epitech_registered_projects(start=monday_of_current_week)
print(f'{len(my_projects)} projets registered:')
for project in my_projects:
    print(project['begin_acti'] + ' - ' + project['end_acti'] + ' -> ' + project['acti_title'])
    add_google_calendar_project(CALENDAR_ID_TIMELINE, project)
