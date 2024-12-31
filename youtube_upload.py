import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

# Set the API scope and credentials
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE = 'client.json'  # Make sure this path is correct
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Authorization process to get the access token
def get_authenticated_service():
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)  # This replaces run_console()
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    # Build the API client
    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    return youtube

# Upload video to YouTube
def upload_video(youtube, video_file, title, description, category_id="22", privacy_status="private"):
    print("Uploading video to YouTube...")
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['test', 'youtube', 'upload'],
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media_file = googleapiclient.http.MediaFileUpload(video_file, resumable=True, mimetype='video/*')

    # Insert video into YouTube
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {status.progress() * 100}%")
    
    print(f"Upload Complete! Video URL: https://www.youtube.com/watch?v={response['id']}")

    
# if __name__ == "__main__":
#     downloaded_video = download_video_from_onedrive()
#     youtube_service = get_authenticated_service()

#     # Provide your video file path and details
#     video_file = downloaded_video  # Replace with your video file
#     title = "Test Video Title"
#     description = "Test video description"
    
#     # Upload the video
#     upload_video(youtube_service, video_file, title, description)

