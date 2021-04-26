from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# init google calendar access

# https://medium.com/@butteredwaffles/working-with-google-calendar-api-8121d5048597

SCOPES = "https://www.googleapis.com/auth/calendar"

store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

service = build('sheets', 'v4', credentials=creds)
