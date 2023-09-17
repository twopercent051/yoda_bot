import asyncio

from apiclient import discovery
from google.oauth2 import service_account

secret_file = "google.json"
sheet_name = "Продажи"
spreadsheet_id = "1z__IxuccSBXOphy0LFHP-HPzim0Ze4MdUcNt8_KKpKE"


class GoogleSheets:

    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
                       "https://www.googleapis.com/auth/spreadsheets"]

        self.credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=self.scopes)
        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)

    async def google_update(self):
        # ranges = ["Продажи!A3:D3"]
        # spreadsheet_info = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id,ranges=ranges
        #                                               ).execute()
        # print(spreadsheet_info)
        ranges = ["Продажи!A:D"]

        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                                      ranges=ranges,
                                                      includeGridData=True).execute()
        # sheet_list = spreadsheet.get("sheets")
        print(len(spreadsheet['sheets'][0]['data'][0]['rowData']))
        for data in spreadsheet['sheets'][0]['data'][0]['rowData']:
            # print(data["values"])

            for cell in data["values"]:
                if cell.__contains__("userEnteredValue"):
                    for k, v in cell["userEnteredValue"].items():
                        print(v)
                else:
                    print(0)
            print("")


if __name__ == "__main__":
    google_sheet = GoogleSheets()
    asyncio.run(google_sheet.google_update())
