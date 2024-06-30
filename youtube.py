from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle

# Initialize the YouTube Data API v3 service
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CREDENTIALS_FILE = 'credentials.pkl'  # File to store/load credentials

def authenticate():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'youtube.json', SCOPES)
        credentials = flow.run_local_server(port=8080)  # Adjust port if necessary
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(credentials, token)
    
    print("Authentication Done")
    return credentials

def build_service():
    credentials = authenticate()
    print("Build Done")
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(file_path, title, description):
   
    youtube = build_service()
    print("Upload Started")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "22",
            "description": description,
            "title": title
          },
          "status": {
            "privacyStatus": "private"
          }
        },
        media_body=MediaFileUpload(file_path)
    )
    response = request.execute()
    print(f"Video upload successful! Video ID: {response['id']}")
    os.remove(file_path)
   



if __name__ == "__main__":
    video_file_path = 'output.mp4'
    video_title = 'Your Video Title'
    video_description = 'Your Video Description'
    upload_video(video_file_path, video_title, video_description)