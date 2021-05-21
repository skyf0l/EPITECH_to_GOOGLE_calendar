#!/usr/bin/env python3

import src.config as config

from src.google_calendar import *

config.load_config_file('config.json')

event_deleted = clear_google_events(config.CALENDAR_ID_EVENTS)
print(f'{event_deleted} events removed')
event_deleted = clear_google_events(config.CALENDAR_ID_TIMELINE)
print(f'{event_deleted} projects removed')
event_deleted = clear_google_events(config.CALENDAR_ID_TEACHING_TEAM)
print(f'{event_deleted} teaching events removed')
event_deleted = clear_google_events(config.CALENDAR_ID_OTHER_CALENDARS)
print(f'{event_deleted} events removed from other calendars')