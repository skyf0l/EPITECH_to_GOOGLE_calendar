#!/usr/bin/env python3

from src.epitech_calendar import *
from src.google_calendar import *


def remove_duplicate_google_events(calendarID, events):
    event_codes = []
    single_events = []
    for event in events:
        event_code = get_google_event_code(event)
        if event_code in event_codes:
            print(f'[-] duplicate {event["summary"]}')
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

    for event in my_events:
        if get_event_code(event) not in google_event_codes:
            # add
            print(f'[+] {event["acti_title"]}')
            add_google_calendar_event(calendarID, event)
            add_event_count += 1
        else:
            # update
            for google_event in google_events:
                if get_event_code(event) == get_google_event_code(google_event):
                    event_start, event_end = get_epitech_event_date(event)
                    google_event_start, google_event_end = get_google_event_date(google_event)
                    if str(event_start) != str(google_event_start) or str(event_end) != str(google_event_end):
                        print(f'[&] date / {google_event["summary"]}')
                        google_event['start']['dateTime'] =  str(event_start).replace(' ', 'T')
                        google_event['start']['timeZone'] = 'Europe/Paris'
                        google_event['end']['dateTime'] =  str(event_end).replace(' ', 'T')
                        google_event['end']['timeZone'] = 'Europe/Paris'
                        service.events().update(calendarId=calendarID, eventId=google_event['id'], body=google_event).execute()
                        update_event_count += 1

    epitech_event_codes = get_event_codes(my_events)
    for google_event in google_events:
        # remove
        if get_google_event_code(google_event) not in epitech_event_codes:
            print(f'[-] {google_event["summary"]}')
            delete_google_event(calendarID, google_event)
            removed_event_count += 1

    if add_event_count != 0 or update_event_count != 0 or removed_event_count != 0:
        print('-> Events summary:')
        if add_event_count != 0:
            print(f'\t{add_event_count} events added')
        if update_event_count != 0:
            print(f'\t{update_event_count} events updated')
        if removed_event_count != 0:
            print(f'\t{removed_event_count} events removed')
    else:
        print('\tUp to date')


def update_projects(calendarID, google_projects, my_projects):
    google_projects = remove_duplicate_google_events(calendarID, google_projects)
    google_project_codes = get_google_event_codes(google_projects)

    add_project_count = 0
    update_project_count = 0
    removed_project_count = 0

    for project in my_projects:
        if get_event_code(project) not in google_project_codes:
            # add
            print(f'[+] {project["acti_title"]}')
            add_google_calendar_project(calendarID, project)
            add_project_count += 1
        else:
            # update
            for google_project in google_projects:
                if get_event_code(project) == get_google_event_code(google_project):
                    event_start, event_end = get_epitech_project_date(project)
                    google_event_start, google_event_end = get_google_event_date(google_project)
                    if str(event_start) != str(google_event_start) or str(event_end) != str(google_event_end):
                        print(f'[&] date / {google_project["summary"]}')
                        google_project['start']['dateTime'] =  str(event_start).replace(' ', 'T')
                        google_project['start']['timeZone'] = 'Europe/Paris'
                        google_project['end']['dateTime'] =  str(event_end).replace(' ', 'T')
                        google_project['end']['timeZone'] = 'Europe/Paris'
                        service.events().update(calendarId=calendarID, eventId=google_project['id'], body=google_project).execute()
                        update_project_count += 1

    epitech_project_codes = get_event_codes(my_projects)
    for google_project in google_projects:
        if get_google_event_code(google_project) not in epitech_project_codes:
            # remove
            print(f'[-] {google_project["summary"]}')
            delete_google_event(calendarID, google_project)
            removed_project_count += 1

    if add_project_count != 0 or update_project_count != 0 or removed_project_count != 0:
        print('-> Projects summary:')
        if add_project_count != 0:
            print(f'\t{add_project_count} projets added')
        if update_project_count != 0:
            print(f'\t{update_project_count} projets updated')
        if removed_project_count != 0:
            print(f'\t{removed_project_count} projets removed')
    else:
        print('\tUp to date')


def update_assistant_events(calendarID, google_assistant_events, my_assistant_events):
    google_assistant_events = remove_duplicate_google_events(calendarID, google_assistant_events)
    google_assistant_event_codes = get_google_event_codes(google_assistant_events)

    add_event_count = 0
    update_event_count = 0
    removed_event_count = 0

    for event in my_assistant_events:
        if get_other_calendars_event_code(event) not in google_assistant_event_codes:
            # add
            print(f'[+] {event["title"]} (id: {event["id"]}, id_calendar: {event["id_calendar"]})')
            add_google_calendar_other_calendars_event(calendarID, event)
            add_event_count += 1
        else:
            # update
            for google_event in google_assistant_events:
                if get_other_calendars_event_code(event) == get_google_event_code(google_event):
                    event_start, event_end = get_epitech_event_date(event)
                    google_event_start, google_event_end = get_google_event_date(google_event)
                    if str(event_start) != str(google_event_start) or str(event_end) != str(google_event_end):
                        print(f'[&] date / {event["title"]} (id: {event["id"]}, id_calendar: {event["id_calendar"]})')
                        google_event['start']['dateTime'] =  str(event_start).replace(' ', 'T')
                        google_event['start']['timeZone'] = 'Europe/Paris'
                        google_event['end']['dateTime'] =  str(event_end).replace(' ', 'T')
                        google_event['end']['timeZone'] = 'Europe/Paris'
                        service.events().update(calendarId=calendarID, eventId=google_event['id'], body=google_event).execute()
                        update_event_count += 1

    epitech_event_codes = get_other_calendars_event_codes(my_assistant_events)
    for google_event in google_assistant_events:
        # remove
        if get_google_event_code(google_event) not in epitech_event_codes:
            print(f'[-] {google_event["summary"]})')
            delete_google_event(calendarID, google_event)
            removed_event_count += 1

    if add_event_count != 0 or update_event_count != 0 or removed_event_count != 0:
        print('-> Events from other calendars summary:')
        if add_event_count != 0:
            print(f'\t{add_event_count} events added')
        if update_event_count != 0:
            print(f'\t{update_event_count} events updated')
        if removed_event_count != 0:
            print(f'\t{removed_event_count} events removed')
    else:
        print('\tUp to date')


def update_other_calendars_events(calendarID, google_events, my_events):
    google_events = remove_duplicate_google_events(calendarID, google_events)
    google_event_codes = get_google_event_codes(google_events)

    add_event_count = 0
    update_event_count = 0
    removed_event_count = 0

    for event in my_events:
        if get_other_calendars_event_code(event) not in google_event_codes:
            # add
            print(f'[+] {event["title"]} (id: {event["id"]}, id_calendar: {event["id_calendar"]})')
            add_google_calendar_other_calendars_event(calendarID, event)
            add_event_count += 1
        else:
            # update
            for google_event in google_events:
                if get_other_calendars_event_code(event) == get_google_event_code(google_event):
                    event_start, event_end = get_epitech_event_date(event)
                    google_event_start, google_event_end = get_google_event_date(google_event)
                    if str(event_start) != str(google_event_start) or str(event_end) != str(google_event_end):
                        print(f'[&] date / {event["title"]} (id: {event["id"]}, id_calendar: {event["id_calendar"]})')
                        google_event['start']['dateTime'] =  str(event_start).replace(' ', 'T')
                        google_event['start']['timeZone'] = 'Europe/Paris'
                        google_event['end']['dateTime'] =  str(event_end).replace(' ', 'T')
                        google_event['end']['timeZone'] = 'Europe/Paris'
                        service.events().update(calendarId=calendarID, eventId=google_event['id'], body=google_event).execute()
                        update_event_count += 1

    epitech_event_codes = get_other_calendars_event_codes(my_events)
    for google_event in google_events:
        # remove
        if get_google_event_code(google_event) not in epitech_event_codes:
            print(f'[-] {google_event["summary"]})')
            delete_google_event(calendarID, google_event)
            removed_event_count += 1

    if add_event_count != 0 or update_event_count != 0 or removed_event_count != 0:
        print('-> Events from other calendars summary:')
        if add_event_count != 0:
            print(f'\t{add_event_count} events added')
        if update_event_count != 0:
            print(f'\t{update_event_count} events updated')
        if removed_event_count != 0:
            print(f'\t{removed_event_count} events removed')
    else:
        print('\tUp to date')
