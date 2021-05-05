#!/usr/bin/env python3

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from src.epitech_calendar import get_epitech_event_date

from datetime import datetime, timedelta

# init google calendar access

# https://medium.com/@butteredwaffles/working-with-google-calendar-api-8121d5048597

SCOPES = 'https://www.googleapis.com/auth/calendar'

store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = build('calendar', 'v3', http=creds.authorize(Http()))


def get_event_location(event):
    if event.get('room') is not None:
        if event['room'].get('code') is not None:
            return event['room']['code']
    return ''


# add event to google calendar

def add_google_calendar_event(calendarID, event):
    event_start, event_end = get_epitech_event_date(event)

    googleEvent = {
        'summary': event['codemodule'] + ' - ' + event['acti_title'],
        'location': get_event_location(event),
        'description': '#event=' + event['codeevent'],
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
        'summary': project['codemodule'] + ' - ' + project['acti_title'],
        'description': '#project=' + project['codeacti'],
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
            if 'description' in event and '#event=' in event['description']:
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
            if 'description' in event and '#project=' in event['description']:
                projects.append(event)
        page_token = google_projects.get('nextPageToken')
        if not page_token:
            break
    return projects