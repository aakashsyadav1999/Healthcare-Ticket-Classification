import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import webbrowser
import streamlit as st

# If modifying these scopes, delete the file token.json.
SCOPES = [
          "https://www.googleapis.com/auth/calendar", 
          "https://www.googleapis.com/auth/calendar.events"
          ]



def auth_calendar_access():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  try:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

  except HttpError as error:
    print(f"An error occurred: {error}")
    
def create_upcoming_events(event):
    """
    Create personalized events on the user's calendar and open the calendar in the web browser.
    """
    try:
      # Call the Calendar API
      auth_calendar_access()
      
      # Create an event
      creds = None
      if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
          token.write(creds.to_json())

      service = build("calendar", "v3", credentials=creds)
      event_result = service.events().insert(calendarId="primary", body=event).execute()
      st.success(f"Event created: {event_result.get('htmlLink')}")
      webbrowser.open(event_result.get('htmlLink'))
          
    except Exception as e:
      print(f"An error occurred: {e}")


    except HttpError as error:
      print(f"An error occurred: {error}")
      
def streamlit_app():
  try:
      st.title("Google Calendar Event Creator")

      st.write("Create a new event on your Google Calendar")

      event_summary = st.text_input("Event Summary", "New Event")
      event_location = st.text_input("Event Location", "Location")
      event_description = st.text_area("Event Description", "Description")
      event_start = st.date_input("Start Date")
      event_start_time = st.time_input("Start Time")
      event_end = st.date_input("End Date")
      event_end_time = st.time_input("End Time")

      if st.button("Create Event"):
        start_datetime = datetime.datetime.combine(event_start, event_start_time).isoformat()
        end_datetime = datetime.datetime.combine(event_end, event_end_time).isoformat()

        event = {
          "summary": event_summary,
          "location": event_location,
          "description": event_description,
          "start": {
            "dateTime": start_datetime,
            "timeZone": "UTC",
          },
          "end": {
            "dateTime": end_datetime,
            "timeZone": "UTC",
          },
        }
        create_upcoming_events(event)

  except HttpError as error:
    st.error(f"An error occurred: {error}")
  

# Run the app
if __name__ == "__main__":
  streamlit_app()