#!/usr/bin/env python3

import json
import requests

from src.google_calendar import *

def get_epitech_login(epitechAutologin):
    url = f'https://intra.epitech.eu/{epitechAutologin}/user/?format=json'
    user_data = requests.get(url).json()
    return user_data['login']


def main():
    epitech_accounts = json.load(open('config.json'))
    for epitech_account in epitech_accounts:

        # config
        EPITECH_AUTOLOGIN = epitech_account['epitech_autologin']
        EPITECH_LOGIN = get_epitech_login(EPITECH_AUTOLOGIN)
        CALENDAR_ID_EVENTS = epitech_account['calendarID_events']
        CALENDAR_ID_TIMELINE = epitech_account['calendarID_timeline']
        CALENDAR_ID_TEACHING_TEAM = epitech_account['calendarID_teaching_team']
        CALENDAR_ID_OTHER_CALENDARS = epitech_account['calendarID_other_calendars']

        print(f'Epitech profile: {EPITECH_LOGIN}')

        if CALENDAR_ID_EVENTS is not None:
            event_deleted = clear_google_events(CALENDAR_ID_EVENTS)
            print(f'-> {event_deleted} events removed from calendarId_events')
        if CALENDAR_ID_TIMELINE is not None:
            event_deleted = clear_google_events(CALENDAR_ID_TIMELINE)
            print(f'-> {event_deleted} events removed from calendarId_timeline')
        if CALENDAR_ID_TEACHING_TEAM is not None:
            event_deleted = clear_google_events(CALENDAR_ID_TEACHING_TEAM)
            print(f'-> {event_deleted} events removed from calendarId_teaching_team')
        if CALENDAR_ID_OTHER_CALENDARS is not None:
            event_deleted = clear_google_events(CALENDAR_ID_OTHER_CALENDARS)
            print(f'-> {event_deleted} events removed from calendarId_other_calendars')

        print()


if __name__ == '__main__':
    main()