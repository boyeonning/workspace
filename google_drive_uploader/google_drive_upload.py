import os
import pickle

import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)

def upload_files(file_path):
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    
    '''
    folder details we want to make
    folder_metadata = {
        "name": "TestFolder",
        "mimeType": "application/vnd.google-apps.folder"
    }
    create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    get the folder id
    folder_id = file.get("id")
    print("Folder ID:", folder_id)
    upload a file text file
    first, define file metadata, such as the name and the parent folder ID'''
    service = get_gdrive_service()
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    file_metadata = {
        "name": file_name,
        "parents": ['1KAOqVploLy5WMuDDx3CCBxge_yeoTGgi'], # 드라이브 폴더 고정
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    # upload
    media = MediaFileUpload(file_path, resumable=True, mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print("File created, id:", file.get("id"))
    return file.get("id")



if __name__ == '__main__': 
    file_path = "/home/jeju/다운로드/[CVSLab]담배자판기 챠트_수정.xlsx" 
    id = upload_files(file_path)
