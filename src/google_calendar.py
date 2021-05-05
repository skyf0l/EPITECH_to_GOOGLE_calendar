from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from src.epitech_calendar import get_epitech_event_date

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