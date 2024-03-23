import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from api_request import fetch_api_data
import logging
import argparse

# Global variable to store event IDs
created_event_ids = []

# Variable to create events
create_events = False

# Variable to delete events after creation
delete_in_sequence = False

# Variable to delete all events with "Deskbee ID:" in their description
delete_all = False

# Variable to update all events
update_all = False

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'calendarapi-418104-ae9899773ec5.json'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fetch API response data
api_response_data = fetch_api_data()

# Load API response data
data = json.loads(api_response_data)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script to import events from Deskbee to Google Calendar')
    parser.add_argument('--create_events', action='store_true', help='Create events in Calendar')
    parser.add_argument('--delete_in_sequence', action='store_true', help='Delete events after creation')
    parser.add_argument('--delete_all', action='store_true', help='Delete all events with "Deskbee ID:" in their description')
    parser.add_argument('--update_all', action='store_true', help='Update all events')
    return parser.parse_args()

def authenticate_google():
    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    return credentials


def update_google_calendar_events(start_date, end_date, area_full, id):
    delete_events_by_deskbee_id()
    create_google_calendar_events(start_date, end_date, area_full, id)

def create_google_calendar_events(start_date, end_date, description, id):

    # Authenticate using the service account
    credentials = authenticate_google()
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Office Day 💼',
        'description': f"• Start Date: {start_date}\n• End Date: {end_date}\n• Area: {description}\n• Deskbee ID: {id}",
        'start': {
            'dateTime': start_date,
            'timeZone': 'GMT-03:00',
        },
        'end': {
            'dateTime': end_date,
            'timeZone': 'GMT-03:00',
        },
        'reminders': {
            'useDefault': True,
        },
        'transparency': 'transparent'
    }

    # Call the Calendar API
    event_response = service.events().insert(calendarId='douglas.odavila@gmail.com', body=event).execute()
    logging.info(f"Creating event for {start_date} to {end_date} in {description}...")
    logging.info(f"Event for {start_date} to {end_date} in {description} created. Event response: {event_response}")
    
    # Store the event ID
    created_event_ids.append(event_response['id'])

def delete_created_events():
    # Wait for a few seconds to ensure events are created before deletion
    time.sleep(5)

    # Authenticate using the service account
    credentials = authenticate_google()
    service = build('calendar', 'v3', credentials=credentials)

    # Iterate through each event ID and delete the corresponding event
    for event_id in created_event_ids:
        service.events().delete(calendarId='douglas.odavila@gmail.com', eventId=event_id).execute()
        logging.info(f"Deleting event with ID {event_id}...")
    
    # Clear the list of created event IDs after deletion
    created_event_ids.clear()

def delete_events_by_deskbee_id():
    # Authenticate using the service account
    credentials = authenticate_google()
    service = build('calendar', 'v3', credentials=credentials)

    # Create a query to search for events with "Deskbee ID:" in the description
    query = "Deskbee ID:"

    # Call the Calendar API
    events_result = service.events().list(calendarId='douglas.odavila@gmail.com', q=query).execute()
    events = events_result.get('items', [])

    # Iterate through each event and delete them
    for event in events:
        event_id = event['id']
        service.events().delete(calendarId='douglas.odavila@gmail.com', eventId=event_id).execute()
        logging.info(f"Deleting event with ID {event_id}...")
    
    # Clear the list of created event IDs after deletion
    created_event_ids.clear()


def main():

    # Parse the command line arguments and set the global variables
    global delete_in_sequence, delete_all, create_events, update_all
    args = parse_arguments()
    create_events = args.create_events
    delete_in_sequence = args.delete_in_sequence
    delete_all = args.delete_all
    update_all = args.update_all

    logging.info("Script started.")

    if create_events:
        for event in data['data']:
            # Extract the date portion from the start_date and end_date strings
            start_date = event['start_date']
            end_date = event['end_date']
            area_full = event['place']['area_full']
            id = event['uuid']
            create_google_calendar_events(start_date, end_date, area_full, id)
    
    if delete_in_sequence:
        # Delete the events created by the script
        delete_created_events()

    if delete_all:
        # Deletes all events with "Deskbee ID:" in their description
        delete_events_by_deskbee_id()

    if update_all:
        logging.info("Updating all events...")
        for event in data['data']:
            # Extract the date portion from the start_date and end_date strings
            start_date = event['start_date']
            end_date = event['end_date']
            area_full = event['place']['area_full']
            id = event['uuid']
            # Updates all events in the calendar
            update_google_calendar_events(start_date, end_date, area_full, id)
        logging.info("Events updated successfully.")

    logging.info("Script completed.")

if __name__ == '__main__':
    main()
