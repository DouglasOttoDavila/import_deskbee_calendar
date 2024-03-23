
# Deskbee Calendar Importer

This script allows you to import events to Google Calendar from a JSON data source.

## Installation
1.  Clone this repository to your local machine:
`git clone https://github.com/yourusername/deskbee-calendar-importer.git` 

2.  Install the required dependencies:
`pip install -r requirements.txt` 

## Usage
Run the script with the following command:

`python importDeskbeeCalendar.py [--create_events] [--delete_in_sequence] [--delete_all] [--update_all]` 
-   `--create_events`:  Create all events in G Calendar, according to the response of Deskbee API.
-   `--delete_in_sequence`: Delete all events after created. Can be used along with `--create_events`.
-   `--delete_all`: Delete events. Standalone.
-   `--update_all`: Delete all events already created in G Calendar and re-create all.

## Configuration
Before running the script, make sure to set up the following:
-   **Service Account Key File**: Place your service account key file (`key.json`) in the root directory of the project.
-   **Google Calendar ID**: Ensure that you're inserting events into the correct Google Calendar. You can find your calendar ID in the Google Calendar settings. (Generally it's your email).

## License
This project is licensed under the MIT License. See the LICENSE file for details.
