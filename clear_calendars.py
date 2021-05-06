#!/usr/bin/env python3

import json

from src.google_calendar import *

config = json.load(open('config.json'))
CALENDAR_ID_EVENTS = config['calendarID_events']
CALENDAR_ID_TIMELINE = config['calendarID_timeline']

event_deleted = clear_google_events(CALENDAR_ID_EVENTS)
print(f'{event_deleted} events removed')
projects_deleted = clear_google_events(CALENDAR_ID_TIMELINE)
print(f'{projects_deleted} events removed')