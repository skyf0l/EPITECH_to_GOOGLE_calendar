#!/usr/bin/env python3

import json

from src.google_calendar import *


def main():
    epitech_accounts = json.load(open('config.json'))
    for epitech_account in epitech_accounts:

        # config
        CALENDAR_ID_EVENTS = epitech_account['calendarID_events']
        CALENDAR_ID_TIMELINE = epitech_account['calendarID_timeline']
        CALENDAR_ID_TEACHING_TEAM = epitech_account['calendarID_teaching_team']
        CALENDAR_ID_OTHER_CALENDARS = epitech_account['calendarID_other_calendars']

        if CALENDAR_ID_EVENTS is not None:
            event_deleted = clear_google_events(CALENDAR_ID_EVENTS, where=lambda event: event.get('description') is not None and re.search('#event=([\w-]*)!', event['description']))
            print(f'-> {event_deleted} events removed from calendarId_events')
        if CALENDAR_ID_TIMELINE is not None:
            event_deleted = clear_google_events(CALENDAR_ID_TIMELINE, where=lambda event: event.get('description') is not None and re.search('#project=([\w-]*)!', event['description']))
            print(f'-> {event_deleted} events removed from calendarId_timeline')
        if CALENDAR_ID_TEACHING_TEAM is not None:
            event_deleted = clear_google_events(CALENDAR_ID_TEACHING_TEAM, where=lambda event: event.get('description') is not None and re.search('#assistant=([\w-]*)!', event['description']))
            print(f'-> {event_deleted} events removed from calendarId_teaching_team')
        if CALENDAR_ID_OTHER_CALENDARS is not None:
            event_deleted = clear_google_events(CALENDAR_ID_OTHER_CALENDARS, where=lambda event: event.get('description') is not None and re.search('#other_calendar_event=([\w-]*)!', event['description']))
            print(f'-> {event_deleted} events removed from calendarId_other_calendars')

        print()


if __name__ == '__main__':
    main()
