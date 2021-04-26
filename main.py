#!/usr/bin/env python3

import os
import requests
from datetime import datetime, timedelta

EPITECH_AUTOLOGIN = os.getenv("EPITECH_AUTOLOGIN")
if EPITECH_AUTOLOGIN is None:
    print("EPITECH_AUTOLOGIN not in env")
    exit(1)

# format: date_from/date_to => 'YYYY-MM-DD'
# get_epitech_events() => current week
# get_epitech_events(from) => all after from included
# get_epitech_events(to) => all in one month before to and to

def get_epitech_events(date_from=None, date_to=None):
    url = f'https://intra.epitech.eu/{EPITECH_AUTOLOGIN}/planning/load?format=json'
    if date_from is not None:
        url += '&start=' + date_from.strftime('%Y-%m-%d')
    if date_to is not None:
        url += '&end=' + date_to.strftime('%Y-%m-%d')
    events = requests.get(url).json()
    return events

# same as get_epitech_events but keep only registered events
# /!\ english delivery not marked as registered

def get_my_epitech_events(date_from=None, date_to=None):
    events = get_epitech_events(date_from=date_from, date_to=date_to)
    print(len(events))
    events_registered = []
    for event in events:
        if 'event_registered' in event and event['event_registered'] is not False:
            events_registered.append(event)
    return events_registered


# update callendar from monday of current week
current_date = datetime.today()
monday_date = current_date - timedelta(days=current_date.weekday())

my_events = get_my_epitech_events(date_from=monday_date)

print(f'{len(my_events)} event registered:')
for event in my_events:
    if 'rdv_group_registered' in event and event['rdv_group_registered'] is not None:
        print('grp ' + event['rdv_group_registered'] +  ' ' + event['acti_title'])
    elif 'rdv_indiv_registered' in event and event['rdv_indiv_registered'] is not None:
        print('ind ' + event['rdv_indiv_registered'] + ' ' + event['acti_title'])
    else:
        print('other ' + event['start'] + '|' + event['end'] + ' ' + event['acti_title'])
