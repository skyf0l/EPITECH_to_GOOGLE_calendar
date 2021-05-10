#!/usr/bin/env python3

import src.config as config
from src.google_calendar import *
from src.epitech_calendar import *
from src.update_calendar import *

from sys import argv
from datetime import datetime, timedelta

# config
config.load_config_file('config.json')

# update callendar from monday of current week from 0 am
if len(argv) == 2:
    current_date = datetime.strptime(argv[1], '%Y-%m-%d')
else:
    current_date = datetime.today()
monday_of_current_week = current_date - timedelta(days=current_date.weekday())
monday_of_current_week = datetime(year=monday_of_current_week.year, month=monday_of_current_week.month, day=monday_of_current_week.day)

google_events = get_google_events(config.CALENDAR_ID_EVENTS, start=monday_of_current_week)
print(f'Already {len(google_events)} events in google calendar')
google_projects = get_google_projects(config.CALENDAR_ID_TIMELINE, start=monday_of_current_week)
print(f'Already {len(google_projects)} projects in google calendar')

my_events = get_my_epitech_events(config.EPITECH_AUTOLOGIN, start=monday_of_current_week)
print(f'{len(my_events)} events registered in epitech calendar')
my_projects = get_my_epitech_projects(config.EPITECH_AUTOLOGIN, start=monday_of_current_week)
print(f'{len(my_projects)} projects registered in epitech calendar')

print()

update_events(config.CALENDAR_ID_EVENTS, google_events, my_events)
print()
update_projects(config.CALENDAR_ID_TIMELINE, google_projects, my_projects)
