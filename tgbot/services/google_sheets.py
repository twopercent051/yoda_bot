import asyncio

from apiclient import discovery
from google.oauth2 import service_account

from create_bot import config


class GoogleSheets:

    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        self.secret_file = config.google.secret_file
        self.credentials = service_account.Credentials.from_service_account_file(self.secret_file, scopes=self.scopes)
        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)
        self.sheet_name = config.google.sheet_name
        self.spreadsheet_id = config.google.spreadsheet_id

    def __get_list(self):
        ranges = [f"{self.sheet_name}!A:G"]
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id,
                                                      ranges=ranges,
                                                      includeGridData=True).execute()
        result = []
        for row in spreadsheet['sheets'][0]['data'][0]['rowData']:
            row_data = []
            for cell in row["values"]:
                value = 0
                if cell.__contains__("userEnteredValue"):
                    for k, v in cell["userEnteredValue"].items():
                        value = v
                row_data.append(value)
            result.append(row_data)
        return result

    def get_user_data(self, phone: str) -> dict:
        all_users = self.__get_list()
        for user in all_users:
            if phone[2:] == str(user[0]):
                data = dict(name=user[1], balance=user[2], status=user[6])
                return data
        return


async def test():
    google_sheet = GoogleSheets()
    a = google_sheet.get_user_data(phone="+79124476847")
    print(a)


if __name__ == "__main__":

    asyncio.run(test())
