import pickle
import os.path
import logging
from typing import List, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)

class GmailHandler:
    def __init__(self):
        print("Initializing GmailHandler...")
        try:
            self.service = self._authenticate()
            print("Successfully authenticated with Gmail API")
            self.labels = self._initialize_labels()
            print("Successfully initialized labels")
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise

    def _authenticate(self) -> any:
        """Handle Gmail API authentication using OAuth2."""
        print("Starting authentication process...")
        creds = None
        if os.path.exists(config.TOKEN_FILE):
            print("Found existing token file")
            with open(config.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            print("Need to refresh or obtain new credentials")
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                print("Getting new credentials")
                if not os.path.exists(config.CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"credentials.json not found. Please ensure it's in the same directory: {os.getcwd()}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.CREDENTIALS_FILE, config.SCOPES)
                creds = flow.run_local_server(port=0)

            print("Saving credentials to token file")
            with open(config.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def _initialize_labels(self) -> dict:
        """Create required labels if they don't exist."""
        try:
            results = self.service.users().labels().list(userId='me').execute()
            existing_labels = {label['name']: label['id'] for label in results['labels']}
            
            required_labels = list(config.CLASSIFICATION_RULES.keys())
            if config.DEFAULT_LABEL:
                required_labels.append(config.DEFAULT_LABEL)
            
            for label_name in required_labels:
                # Skip if label already exists
                if label_name in existing_labels:
                    print(f"Label '{label_name}' already exists")
                    continue
                    
                # Create label with proper formatting
                try:
                    label_body = {
                        'name': label_name,
                        'labelListVisibility': 'labelShow',
                        'messageListVisibility': 'show'
                    }
                    created_label = self.service.users().labels().create(
                        userId='me', body=label_body).execute()
                    existing_labels[label_name] = created_label['id']
                    print(f"Created new label: {label_name}")
                    logging.info(f"Created new label: {label_name}")
                except HttpError as create_error:
                    print(f"Failed to create label '{label_name}': {create_error}")
                    logging.error(f"Failed to create label '{label_name}': {create_error}")
                    # Continue with other labels even if one fails
                    continue

            return existing_labels

        except HttpError as error:
            logging.error(f"Error accessing labels: {error}")
            print(f"Error accessing labels: {error}")
            raise

    def get_recent_emails(self, max_results: int = config.MAX_EMAILS) -> List[dict]:
        """Fetch recent emails from inbox."""
        try:
            results = self.service.users().messages().list(
                userId='me', maxResults=max_results).execute()
            messages = results.get('messages', [])
            
            emails = []
            for message in messages:
                email = self.service.users().messages().get(
                    userId='me', id=message['id']).execute()
                emails.append(email)
            
            return emails

        except HttpError as error:
            logging.error(f"Error fetching emails: {error}")
            return []

    def apply_label(self, email_id: str, label_name: str) -> bool:
        """Apply a label to an email."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': [self.labels[label_name]]}
            ).execute()
            return True
        except HttpError as error:
            logging.error(f"Error applying label {label_name} to email {email_id}: {error}")
            return False 