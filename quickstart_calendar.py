from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import pytz
import calendar


###get time

d = datetime.datetime.now()
u = datetime.timedelta(days=14) 
t = u+d

timezone= pytz.timezone('US/Eastern')
t_end= timezone.localize(t)
t_end=t_end.isoformat('T')

now = datetime.datetime.now()
t_now=timezone.localize(now)
t_now=t_now.isoformat('T')
print("start is :"+str(t_now))
 
print("end is :"+str(t_end))

current_iso_week= datetime.datetime.now().isocalendar()[1]
### 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
#this files uses space not tab
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = '.client_secret_calendar.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def iso_week_num_to_date_range(iso_week, month, year, date_of_work):
    calen = calendar.Calendar()
    calen=list(calen.itermonthdates(year, month))
    #_max_y = len(calen)
    _i=0
     
    week1_start = calen[0]
    week1_end = calen[6]
    week2_start = calen[7]
    week2_end = calen[13]
    week3_start= calen[14]
    week3_end = calen[20]
    week4_start = calen[21]
    week4_end = calen[len(calen)-1]

    print (week1_start, week1_end, week2_start, week2_end, week3_start, week3_end, week4_start, week4_end)
    
    print("date of work is ",date_of_work)
    for i in calen:
        
        if str(i)== date_of_work:
            print ("we got a match")
            
        print(_i)
        if 0<_i<6:
            return str(week1_start)+" to "+str(week1_end)
        elif 7<_i<13:
            return str(week2_start)+" to "+str(week2_end)
        elif 14<_i<20:
            return str(week3_start)+" to "+str(week3_end)
        elif 21<_i<len(calen):
            return str(week4_start)+" to "+str(week4_end)
        _i+=1

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    
    print('Getting the upcoming 15 events')
    #this function returns 15 events by default. 
    eventsResult = service.events().list(
        calendarId='primary', timeMin=t_now, timeMax=t_end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    if not events:
        print('No upcoming events found.')
    i =0
    iso_week1 =0
    iso_week2 =1
    occurance_week1 = 0
    occurance_week2 = 0
    for event in events:
        print('this is '+str(i)+'th event.')
        if event['summary'] == 'MS work':
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start,"--",event['summary'])
 
            work_year,work_month,work_day = start.split('-')

            work_year=int(float(work_year))
            work_month=int(float(work_month))
            work_day=int(float(work_day))

            #print (int(float(work_year)))
            #print (int(float(work_month)))
            #print (int(float(work_day)))

            iso_week= datetime.date(work_year, work_month, work_day).isocalendar()[1]
            #print (iso_week)
            if iso_week == current_iso_week:
                iso_week1=iso_week
                occurance_week1+=1
                week_range1=iso_week_num_to_date_range(iso_week1, work_month, work_year, start)
            if iso_week == current_iso_week+1:
                iso_week2=iso_week
                occurance_week2+=1
                week_range2=iso_week_num_to_date_range(iso_week1, work_month, work_year, start)

            #we ignore anything but the next two weeks.
            
        i+=1
    print ("The first week is week # ",iso_week1,", it is from ",week_range1,". We worked ",occurance_week1," days.")
    print ("The second week is week # ",iso_week2,", it is from ",week_range2,". We worked ",occurance_week2," days.")




if __name__ == '__main__':
    main()
