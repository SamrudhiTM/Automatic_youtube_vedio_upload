# Automatic_youtube_vedio_upload
# OneDrive to YouTube Uploader

This repository contains Python code to download a video from OneDrive and then upload it to YouTube.

**Prerequisites:**

* **Python:** Install Python 3.x on your system.
* **Libraries:** Install required libraries using pip:
  ```bash
  pip install requests webbrowser http.server threading google-api-python-client google-auth-httplib2 google-auth-oauthlib

  Generate API Credentials
1. Microsoft API Credentials (Microsoft Graph API)
To use the Microsoft Graph API and access OneDrive, you need to register an application in the Azure portal and generate API credentials.

Steps to Generate Microsoft API Credentials:
Go to Azure Portal: Open the Azure portal at Azure Portal.
Register an Application:
Navigate to Azure Active Directory > App registrations > New registration.
Enter a name for the application (e.g., "OneDrive Video Uploader").
Choose Accounts in any organizational directory and personal Microsoft accounts for supported account types.
Set the Redirect URI to http://localhost:8080 for local development setup.
Click Register.
Create a Client Secret:
Under the application registration page, go to Certificates & Secrets > New client secret.
Add a description (e.g., "API secret") and set an expiry period.
Copy the Value of the secret (this is your CLIENT_SECRET).
Get Your Application ID:
Under the Overview tab, copy the Application (client) ID.
API Permissions:
Go to API Permissions > Add a permission > Microsoft Graph > Delegated permissions.
Add Files.ReadWrite.All and User.Read for OneDrive access.
Configure Redirect URI:
In the Authentication section, ensure the Redirect URI is configured as http://localhost:8080.
Now, you have the APPLICATION_ID and CLIENT_SECRET which will be used to configure the script.

2. Google API Credentials (YouTube Data API)
To interact with YouTube and upload videos, you need to set up OAuth 2.0 credentials via the Google Developer Console.

Steps to Generate Google API Credentials:
Go to Google Cloud Console: Open the Google Cloud Console at Google Cloud Console.
Create a New Project:
Click on the Select a Project dropdown and then click New Project.
Name the project (e.g., "YouTube Video Uploader").
Enable YouTube Data API:
In the API & Services > Library, search for YouTube Data API v3 and enable it.
Create OAuth 2.0 Credentials:
Navigate to APIs & Services > Credentials > Create Credentials > OAuth 2.0 Client IDs.
Choose Web application as the application type.
Add Authorized redirect URIs: http://localhost:8080 for local development.
Once the credentials are created, copy the Client ID and Client Secret.
Download Client Secret File:
After creating the credentials, download the client_secret.json file and save it in your project directory.
