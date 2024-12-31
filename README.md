# Automatic_youtube_vedio_upload
This project automates the process of downloading video files from OneDrive and uploading them to YouTube using Python. It integrates the Microsoft Graph API for OneDrive access and the YouTube Data API for video uploads.
# OneDrive to YouTube Uploader

This repository contains Python code to download a video from OneDrive and then upload it to YouTube.

**Prerequisites:**

* **Python:** Install Python 3.x on your system.
* **Libraries:** Install required libraries using pip:
  ```bash
  pip install requests webbrowser http.server threading google-api-python-client google-auth-httplib2 google-auth-oauthlib

## Features

- Authenticate with Microsoft OneDrive using the Microsoft Graph API.
- Download videos from OneDrive.
- Authenticate with Google and upload videos to YouTube with customizable metadata.
- Automatically clean up local storage after uploads.

## API Registrations

### 1. Microsoft Graph API (OneDrive Access)
1. Go to the [Microsoft Azure App Registration Portal](https://portal.azure.com/).
2. Register a new application:
   - **Name**: Choose a name for your app.
   - **Supported account types**: Select "Accounts in any organizational directory and personal Microsoft accounts".
   - **Redirect URI**: Add `http://localhost:8000` as a redirect URI.
3. After registration, note down the **Application (client) ID**.
4. Go to **API Permissions**:
   - Add the permission: `Files.ReadWrite`.
   - Grant admin consent if required.

### 2. Google API (YouTube Data API)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **YouTube Data API v3** for your project.
4. Go to **APIs & Services > Credentials**:
   - Create an OAuth 2.0 Client ID:
     - **Application type**: Select "Desktop App".
     - Download the `client.json` file.
5. Save the `client.json` file in the project directory.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/onedrive-to-youtube.git
   cd onedrive-to-youtube


**Configure API credentials:**

Place the client.json file (from Google API setup) in the project root.
Update main.py with your Microsoft Azure client ID.



**Usage**

Authenticate with OneDrive:
The app will open a browser window to authenticate with your Microsoft account.
Select a video file to download from your OneDrive

Authenticate with YouTube:
The app will prompt for Google account authentication.
Allow the application to access your YouTube account.

Video Upload:
The app uploads the video to your YouTube account as a private video with the given title and description.

Clean-Up:
the downloaded video is deleted from local storage after a successful upload.
