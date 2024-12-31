import requests
import os
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Azure app credentials
client_id = "your-client-id"  # Replace with your client ID
tenant_id = "common"  # Use 'common' for personal Microsoft accounts
redirect_uri = "http://localhost:8000"  # Must match the redirect URI in Azure portal
scope = "https://graph.microsoft.com/Files.ReadWrite"

# Global variable to store the downloaded path
downloaded_video_path = None

# Create an event to signal when the server can stop
server_event = threading.Event()

def download_video_from_onedrive():
    global downloaded_video_path  # Use the global variable to store the path

    # Authorization URL
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"

    # Step 1: Get the authorization URL
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    url = f"{auth_url}?{urlencode(params)}"
    webbrowser.open(url)
    
    

    # print(f"Go to the following URL to authenticate: {url}")

    # Step 2: After login, the user is redirected to your redirect URI with a code
    class AuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            global downloaded_video_path  # Access the global variable

            # Extract the authorization code from the URL
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            if "code" in query_params:
                authorization_code = query_params["code"][0]
                # print("Authorization code received:", authorization_code)

                # Step 3: Exchange the code for an access token
                token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
                token_data = {
                    "client_id": client_id,
                    "code": authorization_code,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code"
                }

                response = requests.post(token_url, data=token_data)
                token_json = response.json()

                if "access_token" in token_json:
                    access_token = token_json["access_token"]
                    # print("Access Token:", access_token)

                    # Step 4: Use the access token to list and download OneDrive videos
                    downloaded_video_path = self.list_onedrive_files(access_token)
                    if downloaded_video_path:
                        print(f"Video downloaded to: {downloaded_video_path}")
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(b"Authentication successful! You can close this window.")
                    else:
                        print("No video files found or download failed.")
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(b"Authentication failed! No video found.")

                    # Signal the server to stop after processing the request
                    server_event.set()

            # Default response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this window.")

        def list_onedrive_files(self, access_token):
            download_dir = "C:/Users/acer/drive_upload/downloads"
            os.makedirs(download_dir, exist_ok=True)

            url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_list = response.json()
                video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm']

                for item in file_list.get("value", []):
                    if "file" in item:
                        file_name = item["name"]
                        if any(file_name.endswith(ext) for ext in video_extensions):
                            print(f"Video Found: {file_name}")
                            download_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{item['id']}/content"
                            video_response = requests.get(download_url, headers=headers, stream=True)
                            if video_response.status_code == 200:
                                file_path = os.path.join(download_dir, file_name)
                                with open(file_path, "wb") as f:
                                    for chunk in video_response.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                print(f"Downloaded successfully: {file_path}")
                                return file_path  # Return the full path where the file is downloaded
                            else:
                                print(f"Failed to download {file_name}: {video_response.status_code}")
            else:
                print(f"Error listing files: {response.status_code}")
                print(response.json())
            return None

    # Step 5: Start a local HTTP server to listen for the redirect
    def start_server():
        server_address = ('', 8000)  # Listen on localhost:8000
        httpd = HTTPServer(server_address, AuthHandler)
        print("Server started on http://localhost:8000")
        httpd.handle_request()  # Handle a single request and stop

    # Start the server in a separate thread to allow async operation
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # Allow program to exit even if server is running
    server_thread.start()

    # Wait for the server to process the authentication and set the downloaded path
    server_event.wait()  # Block until the server signals that the task is complete

    return downloaded_video_path  # Return the downloaded video path after server finishes

