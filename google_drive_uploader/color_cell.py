"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
import os
from pprint import pprint
from googleapiclient import discovery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key_1.json"

credentials = None
service = discovery.build('sheets', 'v4', credentials=credentials)

def request_update(spreadsheet_id, sheetid, barcode):
    # The spreadsheet to apply the updates to.
    batch_update_spreadsheet_request_body ={
    "requests": [
        {
        "addConditionalFormatRule": {
            "rule": {
            "ranges": [
                {
                "sheetId": sheetid,
                "startColumnIndex": 1,
                "endColumnIndex": 33,
                },
                {
                "sheetId": sheetid,
                "startColumnIndex": 1,
                "endColumnIndex": 500,
                },
            ],
            "booleanRule": {
                "condition": {
                "type": "TEXT_CONTAINS",
                "values": [
                    {
                    "userEnteredValue": barcode
                    }
                ]
                },
                "format": {
                "backgroundColor": {
                    "red": 221/255,
                    "green": 160/255,
                    "blue" : 221/255,
                }
                }
            }
            },
            "index": 0
        }
        }
    ]
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body)
    response = request.execute()
