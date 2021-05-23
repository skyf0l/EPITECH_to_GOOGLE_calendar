#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta


def get_event_code(event):
    if event.get('codeacti') is not None:
        return event['codeacti']
    if event.get('codeevent') is not None:
        return event['codeevent']
    return None


def get_event_codes(events):
    event_codes = []
    for event in events:
        event_code = get_event_code(event)
        if event_code is not None and event_code not in event_codes:
            event_codes.append(event_code)
    return event_codes


def get_other_calendars_event_code(event):
    return f'{event["id_calendar"]}-{event["id"]}'


def get_other_calendars_event_codes(events):
    event_codes = []
    for event in events:
        event_code = get_other_calendars_event_code(event)
        if event_code not in event_codes:
            event_codes.append(event_code)
    return event_codes


# format: start/end => datetime
# get_all_epitech_events() => all after one month before today
# get_all_epitech_events(start) => all after start
# get_all_epitech_events(end) => all in one month before end and end

def get_all_epitech_events(epitechAutologin, start=None, end=None):
    url = f'https://intra.epitech.eu/{epitechAutologin}/planning/load?format=json'
    if start is not None:
        url += '&start=' + start.strftime('%Y-%m-%d')
    if end is not None:
        url += '&end=' + end.strftime('%Y-%m-%d')
    return requests.get(url).json()


# same as get_all_epitech_events but keep only registered epitech events
# /!\ english delivery not marked as registered

def get_my_epitech_events(epitechAutologin, start=None, end=None):
    events = get_all_epitech_events(epitechAutologin, start=start, end=end)
    events_registered = []
    for event in events:
        if 'scolaryear' in event:
            if 'event_registered' in event and event['event_registered'] not in [None, False]:
                events_registered.append(event)
    return events_registered

# format: start/end => datetime
# get_all_epitech_activities() => current week
# get_all_epitech_activities(start) => all after start included
# get_all_epitech_activities(end) => all in one month before end and end

def get_all_epitech_activities(epitechAutologin, start=None, end=None):
    if start is None and end is None:
        current_date = datetime.today()
        start = current_date - timedelta(days=current_date.weekday())
        end = start + timedelta(weeks=1)
    elif start is None:
        start = end - timedelta(days=31)
    elif end is None:
        end = start + timedelta(days=365)

    url = f'https://intra.epitech.eu/{epitechAutologin}/module/board/?format=json&start={start.strftime("%Y-%m-%d")}&end={end.strftime("%Y-%m-%d")}'
    return requests.get(url).json()


# same as get_all_epitech_activities but keep only registered projects

def get_my_epitech_projects(epitechAutologin, start=None, end=None):
    activities = get_all_epitech_activities(epitechAutologin, start, end)
    projets = []

    for activity in activities:
        if 'registered' in activity and activity['registered'] == 1:
            if 'type_acti_code' in activity and activity['type_acti_code'] == 'proj':
                projets.append(activity)

    return projets


# get all events un a module (module_name is scolaryear/codemodule/codeinstance)

def get_module_activities(epitechAutologin, module_name):
    url = f'https://intra.epitech.eu/{epitechAutologin}/module/{module_name}/?format=json'
    return requests.get(url).json()['activites']


# same as get_all_epitech_activities but keep only assistant events

def get_my_assistant_events(epitechAutologin, start=None, end=None):
    events = get_all_epitech_activities(epitechAutologin, start=start, end=end)
    assistant_events = []

    modules_names = []
    for event in events:
        if 'scolaryear' in event and 'codemodule' in event and 'codeinstance' in event:
            module_name = f'{event["scolaryear"]}/{event["codemodule"]}/{event["codeinstance"]}'
            if module_name not in modules_names:
                modules_names.append(module_name)
    for module_name in modules_names:
        module_activities = get_module_activities(epitechAutologin, module_name)
        for module_activity in module_activities:
            if len(module_activity['events']) > 1:
                print(module_activity['title'], len(module_activity['events']))
    return assistant_events


# same as get_all_epitech_events but keep only other calendar events

def get_epitech_other_calendars_events(epitechAutologin, start=None, end=None):
    events = get_all_epitech_events(epitechAutologin, start=start, end=end)
    other_calendars_events = []
    for event in events:
        if 'id_calendar' in event and 'id' in event:
            other_calendars_events.append(event)
    return other_calendars_events


# same as get_all_epitech_events but keep only registered other calendar events

def get_my_epitech_other_calendars_events(epitechAutologin, start=None, end=None):
    other_calendars_events = get_epitech_other_calendars_events(epitechAutologin, start=start, end=end)
    other_calendars_events_registered = []
    for event in other_calendars_events:
        if 'event_registered' in event and event['event_registered'] not in [None, False]:
            other_calendars_events_registered.append(event)
    return other_calendars_events_registered


# return right (start, end) of event

def get_epitech_event_date(event):
    if 'rdv_group_registered' in event and event['rdv_group_registered'] is not None:
        return event['rdv_group_registered'].split('|')
    elif 'rdv_indiv_registered' in event and event['rdv_indiv_registered'] is not None:
        return event['rdv_indiv_registered'].split('|')
    return event['start'], event['end']


# return right (start, end) of project

def get_epitech_project_date(project):
    return project['begin_acti'], project['end_acti']
