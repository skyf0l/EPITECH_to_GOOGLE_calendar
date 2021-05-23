# EPITECH_to_GOOGLE_calendar

Synchronize your Epitech calendar with Google.

# Features

  - [x] Synchronization of epitech calendar on google calendar
  - [x] Update modified events / Remove canceled events
  - [x] Update modified events
  - [x] Add location and event link of event
  - [x] Display only the selected slot for multi-slots events
  - [x] Project timeline
  - [x] Fetch events the events which you supervise (acti HUB for example)
  - [x] Fetch registered events from private epitech calendars
  - [x] Support multi epitech accounts (very great for AERs who have two epitech accounts and calendars)

# Config

## Python3 - Requirements

```
$ sudo python3 -m pip install -r requirements.txt
```

## Config file

Create a `config.json` file with the following content at root of the repo:

```json
[
    {
        "comment": "student / aer ...",
        "epitech_autologin": "auth-...",
        "calendarID_events": "...@group.calendar.google.com",
        "calendarID_timeline": "...@group.calendar.google.com",
        "calendarID_teaching_team": "...@group.calendar.google.com",
        "calendarID_other_calendars": "...@group.calendar.google.com"
    }
]
```

 - `comment` is what you want, it doesn't matter, it's just useful not to get mixed up if you have multiple accounts
 - `epitech_autologin` is your epitech autologin, you can find it on https://intra.epitech.eu/admin/autolog (copy only `auth-...` part)
 - `calendarID_events` is the calendar in which you want to put all registered events
 - `calendarID_timeline` is the calendar in which you want to put projects timeline
 - `calendarID_teaching_team` is the calendar in which you want to put events which you supervise (acti HUB for example)
 - `calendarID_other_calendars` is the calendar in which you want to put events registered in your private epitech calendars

If you don't want to some events you can set the value of the calendarID to null, and if you want to put all events in only one calendarID you can

## How to get calendarID?

 - Create a calendar in google
 - Go in your new calendar's settings
 - Go in `Integrate Calendar` section
 - Copy `Calendar ID` (in general it looks like `...@group.calendar.google.com`)

# Usage

### Fetch all next events

```
$ python3 main.py
```

### Fetch all events since date

```
$ python3 main.py YYYY-MM-DD
```