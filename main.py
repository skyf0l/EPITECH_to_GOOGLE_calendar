#!/usr/bin/env python3

from src.google_calendar import *
from src.epitech_calendar import *

from sys import argv
from datetime import datetime, timedelta
import os
import json

# config

EPITECH_AUTOLOGIN = os.getenv('EPITECH_AUTOLOGIN')
if EPITECH_AUTOLOGIN is None:
    print('EPITECH_AUTOLOGIN not in env')
    exit(1)

config = json.load(open('config.json'))
CALENDAR_ID_EVENTS = config['calendarID_events']
CALENDAR_ID_TIMELINE = config['calendarID_timeline']


# update callendar from monday of current week from 0 am
if len(argv) == 2:
    current_date = datetime.strptime(argv[1], '%Y-%m-%d')
else:
    current_date = datetime.today()
monday_of_current_week = current_date - timedelta(days=current_date.weekday())
monday_of_current_week = datetime(year=monday_of_current_week.year, month=monday_of_current_week.month, day=monday_of_current_week.day)

google_events = get_google_events(CALENDAR_ID_EVENTS, start=monday_of_current_week)
google_projects = get_google_projects(CALENDAR_ID_TIMELINE, start=monday_of_current_week)

print(f'Already {len(google_events)} events in google calendar')
print(f'Already {len(google_projects)} projects in google calendar')

my_events = get_my_epitech_events(EPITECH_AUTOLOGIN, start=monday_of_current_week)

print(f'{len(my_events)} events registered:')
for event in my_events:
    event_start, event_end = get_epitech_event_date(event)
    print(event_start + ' - ' + event_end + ' -> ' + event['acti_title'])
    add_google_calendar_event(CALENDAR_ID_EVENTS, event)

print()

my_projects = get_my_epitech_registered_projects(EPITECH_AUTOLOGIN, start=monday_of_current_week)
print(f'{len(my_projects)} projets registered:')
for project in my_projects:
    print(project['begin_acti'] + ' - ' + project['end_acti'] + ' -> ' + project['acti_title'])
    add_google_calendar_project(CALENDAR_ID_TIMELINE, project)
