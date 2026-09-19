from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
import keyring
import gspread

# --- Configuration ---
APP_NAME = "MySheetsApp"
CLIENT_SECRET_KEY = "google_oauth_client_secret"
USER_TOKEN_KEY = "google_oauth_user_token"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# --- 1. CLI Credential & OAuth Management ---
def setup_client_secret():
    """First-time CLI setup for the OAuth Client JSON."""
    print("=== First Time Setup ===")
    print("Please paste the contents of your OAuth 2.0 Client ID JSON file.")
    print("Press Enter on an empty line when finished:")
    
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
        
    json_str = "\n".join(lines)
    
    try:
        json.loads(json_str)
        keyring.set_password(APP_NAME, CLIENT_SECRET_KEY, json_str)
        print("Client credentials securely saved!\n")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format. Please restart the app and try again.")
        exit(1)

def get_sheets_client():
    """Authenticate using the real user's Google Account."""
    creds = None
    
    # 1. Check if we already have a saved user token (from a previous login)
    user_token_data = keyring.get_password(APP_NAME, USER_TOKEN_KEY)
    if user_token_data:
        creds = Credentials.from_authorized_user_info(json.loads(user_token_data), SCOPES)
        print(user_token_data)
        
    # 2. If no valid token exists, we must log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Token is expired but can be silently refreshed
            creds.refresh(Request())
        else:
            # Complete first-time setup or full re-authentication
            client_secret_data = keyring.get_password(APP_NAME, CLIENT_SECRET_KEY)
            print(client_secret_data)
            
            if not client_secret_data:
                setup_client_secret()
                client_secret_data = keyring.get_password(APP_NAME, CLIENT_SECRET_KEY)
            
            # Trigger the browser login popup
            client_config = json.loads(client_secret_data)
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Securely save the new/refreshed user token back to the OS
        keyring.set_password(APP_NAME, USER_TOKEN_KEY, creds.to_json())
        
    return gspread.authorize(creds)

if __name__ == "__main__":
    client = get_sheets_client()