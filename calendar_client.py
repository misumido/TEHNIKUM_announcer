from google.oauth2 import service_account
from googleapiclient.discovery import build
class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # Путь ключа от сервис аккаунта
    FILE_PATH = "ecstatic-effort-386311-61b4439f225f.json"

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)
    def get_calendar_list(self):
        return self.service.calendarList().list().execute()
    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }

        return self.service.calendarList().insert(
            body=calendar_list_entry).execute()
    def evenets_list(self):
        page_token = None
        events_summary = []
        while True:
            events = ggl.service.events().list(calendarId="kyhbko@gmail.com", pageToken=page_token).execute()
            for event in events['items']:
                events_summary += [
                    {"Название": event["summary"],
                     "Описание": event["description"],
                     "Дата события": event["start"]["dateTime"][0:10],
                     "Время события": event["start"]["dateTime"][11:16]}
                ]
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return events_summary
ggl = GoogleCalendar()


