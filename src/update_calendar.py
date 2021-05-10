#!/usr/bin/env python3

from src.epitech_calendar import *
from src.google_calendar import *


def remove_duplicate_google_events(calendarID, events):
    event_codes = []
    single_events = []
    for event in events:
        event_code = get_google_event_code(event)
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
    removed_event_count = 0

    print(f'{len(my_events)} events registered:')
    for event in my_events:
        if event['codeacti'] not in google_event_codes:
            event_start, event_end = get_epitech_event_date(event)
            print(f'[+] {event["acti_title"]}')
            add_google_calendar_event(calendarID, event)
            add_event_count += 1

    epitech_event_codes = get_event_codes(my_events)
    for google_event in google_events:
        if get_google_event_code(google_event) not in epitech_event_codes:
            print(f'[-] {google_event["summary"]}')
            delete_google_event(calendarID, google_event)
            removed_event_count += 1

    print('Events summary:')
    print(f'\t{add_event_count} events added')
    print(f'\t{update_event_count} events updated')
    print(f'\t{removed_event_count} events removed')


def update_projects(calendarID, google_projects, my_projects):
    google_projects = remove_duplicate_google_events(calendarID, google_projects)
    google_project_codes = get_google_event_codes(google_projects)

    add_project_count = 0
    update_project_count = 0
    removed_project_count = 0

    print(f'{len(my_projects)} projets registered:')
    for project in my_projects:
        if project['codeacti'] not in google_project_codes:
            print(f'[+] {project["acti_title"]}')
            add_google_calendar_project(calendarID, project)
            add_project_count += 1

    epitech_project_codes = get_event_codes(my_projects)
    for google_project in google_projects:
        if get_google_event_code(google_project) not in epitech_project_codes:
            print(f'[-] {google_project["summary"]}')
            delete_google_event(calendarID, google_project)
            removed_project_count += 1

    print('Projects summary:')
    print(f'\t{add_project_count} projets added')
    print(f'\t{update_project_count} projets updated')
    print(f'\t{removed_project_count} projets removed')
