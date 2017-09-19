from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import quickstart_calendar

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'D:\My Documents\GitHub\GsheetAPI\client_secret_sheets.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

 
  
 

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
                                   'sheets.googleapis.com-python-quickstart.json')
    print(credential_path)
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
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1IaO33cnRu_vVVCjN4yPrGnlUP1t7L46Y7MISAAAIC3c'
    rangeName = 'Invoice!A2:H'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s' %row)


##read Invocie number, increment it
        

##read sheets for week1 # of days and week2 # of days.
    week_range1,week_range2,return_occurance_week1,return_occurance_week2 = quickstart_calendar.main()
    print ("We got the following: "+week_range1,week_range2,return_occurance_week1,return_occurance_week2)

 ##write to sheet example here  


    qty_week1 = return_occurance_week1
    qty_week2 = return_occurance_week2
    values = [[qty_week1],[qty_week2]]
    value_input_option='RAW'
    body = {'values': values}
    rangeName = 'Invoice!E19'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()
    print(result)

    week_range_value=[[week_range1],[week_range2]]
    body = {'values': week_range_value}
    rangeName = 'Invoice!B19'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

    #set invoice ID to be iso_week_value instead, write to cell F12
     
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='Invoice!F12').execute()
    print('Our invoice result is: ',result)
    print('Our invoice result key is values: ',result['values'])
    invoice_ID = int(result['values'][0][0])
    invoice_ID +=1

    print('New ID is ',invoice_ID)
    
    body = {'values': str(invoice_ID)}
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range='Invoice!F12',valueInputOption=value_input_option, body=body).execute()
    #body = {'values': }}

if __name__ == '__main__':
    main()