#!/usr/bin/env python3

import os
import json


EPITECH_AUTOLOGIN = None
CALENDAR_ID_EVENTS = None
CALENDAR_ID_TIMELINE = None
CALENDAR_ID_TEACHING_TEAM = None

def load_config_file(file_path):
    global EPITECH_AUTOLOGIN
    global CALENDAR_ID_EVENTS
    global CALENDAR_ID_TIMELINE
    global CALENDAR_ID_TEACHING_TEAM

    config = json.load(open(file_path))
    EPITECH_AUTOLOGIN = config['epitech_autologin']
    CALENDAR_ID_EVENTS = config['calendarID_events']
    CALENDAR_ID_TIMELINE = config['calendarID_timeline']
    CALENDAR_ID_TEACHING_TEAM = config['calendarID_teaching_team']