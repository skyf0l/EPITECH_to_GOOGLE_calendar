#!/usr/bin/env python3

from src.google_calendar import *
from src.epitech_calendar import *
from src.update_calendar import *

from sys import argv
from datetime import datetime, timedelta
import json


def get_epitech_login(epitechAutologin):
    url = f'https://intra.epitech.eu/{epitechAutologin}/user/?format=json'
    user_data = requests.get(url).json()
    return user_data['login']


# update callendar from monday of current week from 0 am
if len(argv) == 2:
    current_date = datetime.strptime(argv[1], '%Y-%m-%d')
else:
    current_date = datetime.today()
monday_of_current_week = current_date - timedelta(days=current_date.weekday())
monday_of_current_week = datetime(year=monday_of_current_week.year, month=monday_of_current_week.month, day=monday_of_current_week.day)

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

    # update calendars
    if CALENDAR_ID_EVENTS is not None:
        google_events = get_google_events(CALENDAR_ID_EVENTS, start=monday_of_current_week)
        print(f'-> Already {len(google_events)} events in google calendar')
        my_events = get_my_epitech_events(EPITECH_AUTOLOGIN, start=monday_of_current_week)
        print(f'-> {len(my_events)} events registered in epitech calendar')
        update_events(CALENDAR_ID_EVENTS, google_events, my_events)

    if CALENDAR_ID_TIMELINE is not None:
        google_projects = get_google_projects(CALENDAR_ID_TIMELINE, start=monday_of_current_week)
        print(f'-> Already {len(google_projects)} projects in google calendar')
        my_projects = get_my_epitech_projects(EPITECH_AUTOLOGIN, start=monday_of_current_week)
        print(f'-> {len(my_projects)} projects registered in epitech calendar')
        update_projects(CALENDAR_ID_TIMELINE, google_projects, my_projects)

    if CALENDAR_ID_TEACHING_TEAM is not None:
        google_assistant_events = get_google_assistant_events(CALENDAR_ID_TEACHING_TEAM, start=monday_of_current_week)
        print(f'-> Already {len(google_assistant_events)} assistant events in google calendar')
        my_google_assistant_events = get_my_assistant_events(EPITECH_AUTOLOGIN, start=monday_of_current_week)
        print(f'-> {len(my_google_assistant_events)} assistant events registered in epitech calendar')
        update_assistant_events(CALENDAR_ID_TIMELINE, google_assistant_events, my_google_assistant_events)

    if CALENDAR_ID_OTHER_CALENDARS is not None:
        google_other_calendars_events = get_google_other_calendars_events(CALENDAR_ID_OTHER_CALENDARS, start=monday_of_current_week)
        print(f'-> Already {len(google_other_calendars_events)} events registered in other calendars in google calendar')
        my_other_calendars_events = get_my_epitech_other_calendars_events(EPITECH_AUTOLOGIN, start=monday_of_current_week)
        print(f'-> {len(my_other_calendars_events)} events registered in other epitech calendars')
        update_other_calendars_events(CALENDAR_ID_OTHER_CALENDARS, google_other_calendars_events, my_other_calendars_events)

    print()
