#!/usr/bin/env python3

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from src.epitech_calendar import get_epitech_event_date

from datetime import datetime, timedelta
import re

# init google calendar access

# https://medium.com/@butteredwaffles/working-with-google-calendar-api-8121d5048597

SCOPES = 'https://www.googleapis.com/auth/calendar'

store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = build('calendar', 'v3', http=creds.authorize(Http()))


def get_google_event_code(googleEvent):
    match = re.search('#(?:event|project)=([\w-]*)!', googleEvent['description'])
    if match is None or len(match.groups()) != 1:
        return None
    return match.groups()[0]


def get_google_event_codes(events):
    event_codes = []
    for event in events:
        event_code = get_google_event_code(event)
        if event_code not in event_codes:
            event_codes.append(event_code)
    return event_codes


def get_event_location(event):
    if event.get('room') is not None:
        if event['room'].get('code') is not None:
            return event['room']['code']
    return ''


def make_event_description(event):
    description = ''

    if event.get('scolaryear') and event.get('codemodule') and event.get('codeinstance') and event.get('codeacti'):
        event_url = f"https://intra.epitech.eu/module/{event['scolaryear']}/{event['codemodule']}/{event['codeinstance']}/{event['codeacti']}/"
        description += f"<a href=\"{event_url}\">Link {event['acti_title']}</a>"
        description += '<br>'

    description += f"#event={event['codeacti']}!"
    return description


def make_project_description(project):
    description = ''

    if project.get('scolaryear') and project.get('codemodule') and project.get('codeinstance') and project.get('codeacti'):
        event_url = f"https://intra.epitech.eu/module/{project['scolaryear']}/{project['codemodule']}/{project['codeinstance']}/{project['codeacti']}/project/#!/group"
        description += f"<a href=\"{event_url}\">Link {project['acti_title']}</a>"
        description += '<br>'

    description += f"#project={project['codeacti']}!"
    return description


# add event to google calendar

def add_google_calendar_event(calendarID, event):
    event_start, event_end = get_epitech_event_date(event)

    googleEvent = {
        'summary': event['codemodule'] + ' >> ' + event['acti_title'],
        'location': get_event_location(event),
        'description': make_event_description(event),
        'start': {
            'dateTime': event_start.replace(' ', 'T'),
            'timeZone': 'Europe/Paris'
        },
        'end': {
            'dateTime': event_end.replace(' ', 'T'),
            'timeZone': 'Europe/Paris'
        },
    }
    service.events().insert(calendarId=calendarID, body=googleEvent).execute()


# add project to google calendar

def add_google_calendar_project(calendarID, project):
    googleEvent = {
        'summary': project['codemodule'] + ' >> ' + project['acti_title'],
        'description': make_project_description(project),
        'start': {
            'dateTime': project['begin_acti'].replace(' ', 'T'),
            'timeZone': 'Europe/Paris'
        },
        'end': {
            'dateTime': project['end_acti'].replace(' ', 'T'),
            'timeZone': 'Europe/Paris'
        },
    }
    service.events().insert(calendarId=calendarID, body=googleEvent).execute()


# get events from google calendar

def get_google_events(calendarID, start=None, end=None):
    if start is None and end is None:
        current_date = datetime.today()
        start = current_date - timedelta(days=current_date.weekday())
        end = start + timedelta(weeks=1)
    elif start is None:
        start = end - timedelta(days=31)
    elif end is None:
        end = start + timedelta(days=365)
    start = start.isoformat() + 'Z'
    end = end.isoformat() + 'Z'

    events = []

    page_token = None
    while True:
        google_events = service.events().list(calendarId=calendarID, pageToken=page_token,
                                              timeZone='Europe/Paris', timeMin=start, timeMax=end).execute()
        for event in google_events['items']:
            if 'description' in event and re.search('#event=[\w-]*!', event['description']) is not None:
                events.append(event)
        page_token = google_events.get('nextPageToken')
        if not page_token:
            break
    return events


# get projects from google calendar

def get_google_projects(calendarID, start=None, end=None):
    if start is None and end is None:
        current_date = datetime.today()
        start = current_date - timedelta(days=current_date.weekday())
        end = start + timedelta(weeks=1)
    elif start is None:
        start = end - timedelta(days=31)
    elif end is None:
        end = start + timedelta(days=365)
    start = start.isoformat() + 'Z'
    end = end.isoformat() + 'Z'

    projects = []

    page_token = None
    while True:
        google_projects = service.events().list(calendarId=calendarID, pageToken=page_token,
                                              timeZone='Europe/Paris', timeMin=start, timeMax=end).execute()
        for event in google_projects['items']:
            if 'description' in event and re.search('#project=[\w-]*!', event['description']) is not None:
                projects.append(event)
        page_token = google_projects.get('nextPageToken')
        if not page_token:
            break
    return projects


# delete event from google calendar

def delete_google_event(calendarID, googleEvent):
    eventID = googleEvent['id']
    service.events().delete(calendarId=calendarID, eventId=eventID, sendNotifications=False).execute()


# delete events from google calendar

def delete_google_events(calendarID, googleEvents):
    count = 0
    for googleEvent in googleEvents:
        delete_google_event(calendarID, googleEvent)
        count += 1
    return count


# clear all events from google calendar

def clear_google_events(calendarID):
    count = 0
    page_token = None
    while True:
        google_projects = service.events().list(calendarId=calendarID, pageToken=page_token).execute()
        count += delete_google_events(calendarID, google_projects['items'])
        page_token = google_projects.get('nextPageToken')
        if not page_token:
            break
    return count