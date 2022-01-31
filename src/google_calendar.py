#!/usr/bin/env python3

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from src.epitech_calendar import get_epitech_event_date

from datetime import datetime, timedelta
import re

from src.epitech_calendar import *

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
    match = re.search('#(?:event|project|assistant|other_calendar_event)=([\w-]+)!', googleEvent['description'])
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
    if event.get('location') is not None:
        return event['location']
    return ''


def make_event_description(accountLogin, event):
    description = ''

    if event.get('scolaryear') and event.get('codemodule') and event.get('codeinstance') and get_event_code(event):
        event_url = f"https://intra.epitech.eu/module/{event['scolaryear']}/{event['codemodule']}/{event['codeinstance']}/{get_event_link_code(event)}/"
        description += f"<b>Link</b>: <a href=\"{event_url}\">{event['acti_title']}</a>"
        description += '<br>'

    if event.get('prof_inst') is not None:
        teaching_teams = []
        for teaching_team in event['prof_inst']:
            if teaching_team.get('type') == 'user':
                teaching_teams.append(teaching_team['login'])

        if len(teaching_teams) != 0:
            description += '<br>'
            description += '<b>Teaching teams:</b><br>\t'
            description += '<br>\t'.join(teaching_teams)
            description += '<br>'

    description += '<br>'
    description += f'#accountLogin={accountLogin}!<br>'
    description += f'#event={get_event_code(event)}!'
    return description


def make_project_description(accountLogin, project):
    description = ''

    if project.get('scolaryear') and project.get('codemodule') and project.get('codeinstance') and get_event_code(project):
        event_url = f"https://intra.epitech.eu/module/{project['scolaryear']}/{project['codemodule']}/{project['codeinstance']}/{get_event_link_code(project)}/project/#!/group"
        description += f"<b>Link</b>: <a href=\"{event_url}\">{project['acti_title']}</a>"
        description += '<br>'

    description += '<br>'
    description += f'#accountLogin={accountLogin}!<br>'
    description += f'#project={get_event_code(project)}!'
    return description


def make_assistant_description(accountLogin, event):
    description = ''

    if event.get('scolaryear') and event.get('codemodule') and event.get('codeinstance') and get_event_code(event):
        event_url = f"https://intra.epitech.eu/module/{event['scolaryear']}/{event['codemodule']}/{event['codeinstance']}/{get_event_link_code(event)}/"
        description += f"<b>Link</b>: <a href=\"{event_url}\">{event['acti_title']}</a>"
        description += '<br>'

    if event.get('prof_inst') is not None:
        teaching_teams = []
        for teaching_team in event['prof_inst']:
            if teaching_team.get('type') == 'user':
                teaching_teams.append(teaching_team['login'])

        if len(teaching_teams) != 0:
            description += '<br>'
            description += '<b>Teaching teams:</b><br>\t'
            description += '<br>\t'.join(teaching_teams)
            description += '<br>'

    description += '<br>'
    description += f'#accountLogin={accountLogin}!<br>'
    description += f'#assistant={get_event_code(event)}!'
    return description


def make_other_calendar_event_description(accountLogin, event):
    description = ''

    if event.get('id') and event.get('id_calendar'):
        event_url = f"https://intra.epitech.eu/planning/{event['id_calendar']}/{event['id']}/"
        description += f"<b>Link</b>: <a href=\"{event_url}\">{event['title']}</a>"
        description += '<br>'

    if event.get('description') and len(event['description']) != 0:
        description += event['description']
        description += '<br>'

    description += '<br>'
    description += f'#accountLogin={accountLogin}!<br>'
    description += f"#other_calendar_event={event['id_calendar']}-{event['id']}!"
    return description


# add event to google calendar

def add_google_calendar_event(calendarID, accountLogin, event):
    event_start, event_end = get_epitech_event_date(event)

    googleEvent = {
        'summary': event['codemodule'] + ' >> ' + event['acti_title'],
        'location': get_event_location(event),
        'description': make_event_description(accountLogin, event),
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

def add_google_calendar_project(calendarID, accountLogin, project):
    googleEvent = {
        'summary': project['codemodule'] + ' >> ' + project['acti_title'],
        'description': make_project_description(accountLogin, project),
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


# add event to google calendar

def add_google_calendar_assistant(calendarID, accountLogin, event):
    event_start, event_end = get_epitech_event_date(event)

    googleEvent = {
        'summary': event['codemodule'] + ' >> ' + event['acti_title'],
        'location': get_event_location(event),
        'description': make_assistant_description(accountLogin, event),
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


# add other calendars event to google calendar

def add_google_calendar_other_calendars_event(calendarID, accountLogin, event):
    googleEvent = {
        'summary': event['title'],
        'location': get_event_location(event),
        'description': make_other_calendar_event_description(accountLogin, event),
        'start': {
            'dateTime': event['start'].replace(' ', 'T'),
            'timeZone': 'Europe/Paris'
        },
        'end': {
            'dateTime': event['end'].replace(' ', 'T'),
            'timeZone': 'Europe/Paris'
        },
    }
    service.events().insert(calendarId=calendarID, body=googleEvent).execute()


def get_google_activities(calendarID, accountLogin, code, start=None, end=None):
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
            if 'description' in event:
                if re.search(f'#accountLogin=(?:<a.*>)?{accountLogin}(?:<\/a>)?!', event['description']) and re.search(f'#{code}=[\\w-]*!', event['description']):
                    events.append(event)
        page_token = google_events.get('nextPageToken')
        if not page_token:
            break
    return events

# get events from google calendar


def get_google_events(calendarID, accountLogin, start=None, end=None):
    return get_google_activities(calendarID, accountLogin, 'event', start, end)


# get projects from google calendar

def get_google_projects(calendarID, accountLogin, start=None, end=None):
    return get_google_activities(calendarID, accountLogin, 'project', start, end)


# get assistant events from google calendar

def get_google_assistant_events(calendarID, accountLogin, start=None, end=None):
    return get_google_activities(calendarID, accountLogin, 'assistant', start, end)


# get other calendars events from google calendar

def get_google_other_calendars_events(calendarID, accountLogin, start=None, end=None):
    return get_google_activities(calendarID, accountLogin, 'other_calendar_event', start, end)


# return right (start, end) of event

def get_google_event_date(event):
    start = datetime.strptime(event['start']['dateTime'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
    end = datetime.strptime(event['end']['dateTime'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
    return start, end


# delete event from google calendar

def delete_google_event(calendarID, googleEvent):
    eventID = googleEvent['id']
    service.events().delete(calendarId=calendarID, eventId=eventID, sendNotifications=False).execute()


# delete events from google calendar

def delete_google_events(calendarID, googleEvents, where=None):
    count = 0
    for googleEvent in googleEvents:
        if where is None or where(googleEvent):
            delete_google_event(calendarID, googleEvent)
            count += 1
    return count


# clear all events from google calendar

def clear_google_events(calendarID, where=None):
    count = 0
    page_token = None
    while True:
        google_projects = service.events().list(calendarId=calendarID, pageToken=page_token).execute()
        count += delete_google_events(calendarID, google_projects['items'], where)
        page_token = google_projects.get('nextPageToken')
        if not page_token:
            break
    return count
