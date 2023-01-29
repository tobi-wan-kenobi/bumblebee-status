"""Displays first upcoming event in google calendar.

Events that are set as 'all-day' will not be shown.

Requires credentials.json from a google api application where the google calendar api is installed.
On first time run the browser will open and google will ask for permission for this app to access
the google calendar and then save a .gcalendar_token.json file to the credentials_path directory
which stores this permission.

A refresh is done every 15 minutes.

Parameters:
    * gcalendar.time_format: Format time output. Defaults to "%H:%M".
    * gcalendar.date_format: Format date output. Defaults to "%d.%m.%y".
    * gcalendar.credentials_path: Path to credentials.json. Defaults to "~/".
    * gcalendar.locale: locale to use rather than the system default.

Requires these pip packages:
   * google-api-python-client >= 1.8.0
   * google-auth-httplib2
   * google-auth-oauthlib
"""

# This import belongs to the google code
from __future__ import print_function

from dateutil.parser import parse as dtparse

import core.module
import core.widget
import core.decorators
import util.format

import datetime
import os.path
import locale
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Minutes
update_every = 15


class Module(core.module.Module):
    @core.decorators.every(minutes=update_every)
    def __init__(self, config, theme):
        super().__init__(config, theme, [core.widget.Widget(self.__datetime), core.widget.Widget(self.__summary)])
        self.__error = False
        self.__time_format = self.parameter("time_format", "%H:%M")
        self.__date_format = self.parameter("date_format", "%d.%m.%y")
        self.__credentials_path = os.path.expanduser(
            self.parameter("credentials_path", "~/")
        )
        self.__credentials = os.path.join(self.__credentials_path, "credentials.json")
        self.__token = os.path.join(self.__credentials_path, ".gcalendar_token.json")

        l = locale.getdefaultlocale()
        if not l or l == (None, None):
            l = ("en_US", "UTF-8")
        lcl = self.parameter("locale", ".".join(l))
        try:
            locale.setlocale(locale.LC_TIME, lcl.split("."))
        except Exception:
            locale.setlocale(locale.LC_TIME, ("en_US", "UTF-8"))

        self.__last_update = time.time()
        self.__gcalendar_date, self.__gcalendar_summary = self.__fetch_from_calendar()

    def hidden(self):
        return self.__error

    def __datetime(self, _):
        return self.__gcalendar_date

    @core.decorators.scrollable
    def __summary(self, _):
        return self.__gcalendar_summary


    def __fetch_from_calendar(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

        creds = None

        try:
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists(self.__token):
                creds = Credentials.from_authorized_user_file(self.__token, SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.__credentials, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(self.__token, "w") as token:
                    token.write(creds.to_json())

            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            end = (
                datetime.datetime.utcnow() + datetime.timedelta(days=7)
            ).isoformat() + "Z"  # 'Z' indicates UTC time
            # Get all calendars
            calendar_list = service.calendarList().list().execute()
            event_list = []
            for calendar_list_entry in calendar_list["items"]:
                calendar_id = calendar_list_entry["id"]
                events_result = (
                    service.events()
                    .list(
                        calendarId=calendar_id,
                        timeMin=now,
                        timeMax=end,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])

                for event in events:
                    start = dtparse(
                        event["start"].get("dateTime", event["start"].get("date"))
                    )
                    # Only add to list if not an whole day event
                    if start.tzinfo:
                        event_list.append(
                            {
                                "date": start,
                                "summary": event["summary"],
                                "type": event["eventType"],
                            }
                        )
            sorted_list = sorted(event_list, key=lambda t: t["date"])
            next_event = sorted_list[0]

            if next_event["date"] >= datetime.datetime.now(datetime.timezone.utc):
                if next_event["date"].date() == datetime.datetime.utcnow().date():
                    dt = next_event["date"].astimezone()\
                            .strftime(f"{self.__time_format}")
                else:
                    dt = next_event["date"].astimezone()\
                            .strftime(f"{self.__date_format} {self.__time_format}")
                return (dt, next_event["summary"])

            return (None, "No upcoming events.")
        except:
            self.__error = True

    def update(self):
        # Since scrolling runs the update command and therefore negates the
        # every decorator, this need to be stopped
        # to not break the API rules of google.
        if self.__last_update+(update_every*60) < time.time():
            self.__last_update = time.time()
            self.__gcalendar_date, self.__gcalendar_summary = self.__fetch_from_calendar()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
