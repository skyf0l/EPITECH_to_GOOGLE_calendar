#!/usr/bin/env python3

import requests
import json


EPITECH_AUTOLOGIN = None
EPITECH_LOGIN = None
CALENDAR_ID_EVENTS = None
CALENDAR_ID_TIMELINE = None
CALENDAR_ID_TEACHING_TEAM = None
CALENDAR_ID_OTHER_CALENDARS = None


def get_epitech_login(epitechAutologin):
    url = f'https://intra.epitech.eu/{epitechAutologin}/user/?format=json'
    user_data = requests.get(url).json()
    return user_data['login']


def load_config_file(file_path):
    global EPITECH_AUTOLOGIN
    global EPITECH_LOGIN
    global CALENDAR_ID_EVENTS
    global CALENDAR_ID_TIMELINE
    global CALENDAR_ID_TEACHING_TEAM
    global CALENDAR_ID_OTHER_CALENDARS

    config = json.load(open(file_path))
    EPITECH_AUTOLOGIN = config['epitech_autologin']
    EPITECH_LOGIN = get_epitech_login(EPITECH_AUTOLOGIN)
    CALENDAR_ID_EVENTS = config['calendarID_events']
    CALENDAR_ID_TIMELINE = config['calendarID_timeline']
    CALENDAR_ID_TEACHING_TEAM = config['calendarID_teaching_team']
    CALENDAR_ID_OTHER_CALENDARS = config['calendarID_other_calendars']