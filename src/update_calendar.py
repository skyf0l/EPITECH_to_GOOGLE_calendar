#!/usr/bin/env python3

from src.google_calendar import *


def get_event_code(googleEvent):
    match = re.search('#(?:event|project)=([\w-]*)!', googleEvent['description'])
    if match is None or len(match.groups()) != 1:
        return None
    return match.groups()[0]


def get_google_event_codes(events):
    event_codes = []
    for event in events:
        event_code = get_event_code(event)
        if event_code not in event_codes:
            event_codes.append(event_code)
    return event_codes


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
    google_event_codes = get_google_event_codes(google_events)

    add_event_count = 0
    update_event_count = 0

    print(f'{len(my_events)} events registered:')
    for event in my_events:
        if event['codeacti'] not in google_event_codes:
            event_start, event_end = get_epitech_event_date(event)
            print(event_start + ' - ' + event_end + ' -> ' + event['acti_title'])
            add_google_calendar_event(calendarID, event)
            add_event_count += 1

    print(f'{add_event_count} events added')
    print(f'{update_event_count} events updated')


def update_projects(calendarID, google_projects, my_projects):
    google_projects = remove_duplicate_google_events(calendarID, google_projects)
    google_project_codes = get_google_event_codes(google_projects)

    add_project_count = 0
    update_project_count = 0

    print(f'{len(my_projects)} projets registered:')
    for project in my_projects:
        if project['codeacti'] not in google_project_codes:
            print(project['begin_acti'] + ' - ' + project['end_acti'] + ' -> ' + project['acti_title'])
            add_google_calendar_project(calendarID, project)
            add_project_count += 1

    print(f'{add_project_count} projets added')
    print(f'{update_project_count} projets updated')
