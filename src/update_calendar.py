#!/usr/bin/env python3

from src.google_calendar import *


def get_event_code(googleEvent):
    match = re.search('#(?:event|project)=([\w-]*)!', googleEvent['description'])
    if match is None or len(match.groups()) != 1:
        return None
    return match.groups()[0]


def remove_duplicate_google_events(calendarID, events):
    event_codes = []
    single_events = []
    for event in events:
        event_code = get_event_code(event)
        if event_code in event_codes:
            delete_google_event(calendarID, event)
        else:
            event_codes.append(event_code)
            single_events.append(event)
    return single_events


def update_events(calendarID, google_events, my_events):
    google_events = remove_duplicate_google_events(calendarID, google_events)
    print(f'{len(my_events)} events registered:')
    for event in my_events:
        event_start, event_end = get_epitech_event_date(event)
        print(event_start + ' - ' + event_end + ' -> ' + event['acti_title'])
        add_google_calendar_event(calendarID, event)


def update_projects(calendarID, google_projects, my_projects):
    google_projects = remove_duplicate_google_events(calendarID, google_projects)
    print(f'{len(my_projects)} projets registered:')
    for project in my_projects:
        print(project['begin_acti'] + ' - ' + project['end_acti'] + ' -> ' + project['acti_title'])
        add_google_calendar_project(calendarID, project)
