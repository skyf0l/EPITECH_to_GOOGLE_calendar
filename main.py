#!/usr/bin/env python3

from src.google_calendar import *
from src.epitech_calendar import *
from src.update_calendar import *

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
CALENDAR_ID_TEACHING_TEAM = config['calendarID_teaching_team']

# update callendar from monday of current week from 0 am
if len(argv) == 2:
    current_date = datetime.strptime(argv[1], '%Y-%m-%d')
else:
    current_date = datetime.today()
monday_of_current_week = current_date - timedelta(days=current_date.weekday())
monday_of_current_week = datetime(year=monday_of_current_week.year, month=monday_of_current_week.month, day=monday_of_current_week.day)

google_events = get_google_events(CALENDAR_ID_EVENTS, start=monday_of_current_week)
print(f'Already {len(google_events)} events in google calendar')
google_projects = get_google_projects(CALENDAR_ID_TIMELINE, start=monday_of_current_week)
print(f'Already {len(google_projects)} projects in google calendar')

my_events = get_my_epitech_events(EPITECH_AUTOLOGIN, start=monday_of_current_week)
print(f'{len(my_events)} events registered in epitech calendar')
my_projects = get_my_epitech_projects(EPITECH_AUTOLOGIN, start=monday_of_current_week)
print(f'{len(my_projects)} projects registered in epitech calendar')

print()

update_events(CALENDAR_ID_EVENTS, google_events, my_events)
print()
update_projects(CALENDAR_ID_TIMELINE, google_projects, my_projects)
