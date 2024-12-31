from drive_download import download_video_from_onedrive
from youtube_upload import get_authenticated_service, upload_video
import os

def main():
    # Step 1: Download the video from OneDrive
    downloaded_video = download_video_from_onedrive()
    print(f"Downloaded video path: {downloaded_video}")  # Debugging line
    
    if downloaded_video:
        # Step 2: Get the authenticated YouTube service
        youtube_service = get_authenticated_service()

        # Step 3: Define the video details
        title = "Test Video Title"
        description = "Test video description"
        
        # Step 4: Upload the video
        print("Starting video upload...")  # Debugging line
        upload_video(youtube_service, downloaded_video, title, description)
        
        if os.path.exists(downloaded_video):
            os.remove(downloaded_video)
            print(" deleted from local storage.")

if __name__ == "__main__":
    main()
