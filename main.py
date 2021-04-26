#!/usr/bin/env python3

from sys import argv
import os
import requests
from datetime import datetime, timedelta

EPITECH_AUTOLOGIN = os.getenv("EPITECH_AUTOLOGIN")
if EPITECH_AUTOLOGIN is None:
    print("EPITECH_AUTOLOGIN not in env")
    exit(1)


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

# update callendar from monday of current week
if len(argv) == 2:
    current_date = datetime.strptime(argv[1], '%Y-%m-%d')
else:
    current_date = datetime.today()
monday_of_current_week = current_date - timedelta(days=current_date.weekday())

my_events = get_my_epitech_events(start=monday_of_current_week)

print(f'{len(my_events)} events registered:')
for event in my_events:
    if 'rdv_group_registered' in event and event['rdv_group_registered'] is not None:
        event_start, event_end = event['rdv_group_registered'].split('|')
    elif 'rdv_indiv_registered' in event and event['rdv_indiv_registered'] is not None:
        event_start, event_end = event['rdv_indiv_registered'].split('|')
    else:
        event_start = event['start']
        event_end = event['end']
    
    print(event_start + ' - ' + event_end + ' -> ' + event['acti_title'])

print()

my_projects = get_my_epitech_registered_projects(start=monday_of_current_week)
print(f'{len(my_projects)} projets registered:')
for project in my_projects:
    print(project['begin_acti'] + ' - ' + project['end_acti'] + ' -> ' + project['acti_title'])
