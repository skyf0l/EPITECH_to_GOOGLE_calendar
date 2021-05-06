#!/usr/bin/env python3

from src.google_calendar import *


def update_events(calendarID, google_events, my_events):
    print(f'{len(my_events)} events registered:')
    for event in my_events:
        event_start, event_end = get_epitech_event_date(event)
        print(event_start + ' - ' + event_end + ' -> ' + event['acti_title'])
        add_google_calendar_event(calendarID, event)


def update_projects(calendarID, google_projects, my_projects):
    print(f'{len(my_projects)} projets registered:')
    for project in my_projects:
        print(project['begin_acti'] + ' - ' + project['end_acti'] + ' -> ' + project['acti_title'])
        add_google_calendar_project(calendarID, project)
