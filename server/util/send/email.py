import os
import base64
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text, file_paths=None):
    if file_paths:
        message = MIMEMultipart()
        message.attach(MIMEText(message_text))
    else:
        message = MIMEText(message_text)

    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    if file_paths:
        for file_path in file_paths:
            content_type, encoding = mimetypes.guess_type(file_path)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)

            with open(file_path, 'rb') as file:
                attachment = MIMEBase(main_type, sub_type)
                attachment.set_payload(file.read())

            encoders.encode_base64(attachment)
            file_name = os.path.basename(file_path)
            attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
            message.attach(attachment)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {message['id']}")
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    service = get_gmail_service()
    sender = "your_email@gmail.com"
    to = "pranavkolte111@gmail.com"
    subject = "Test Email from Gmail API"
    message_text = "This is a test email sent using the Gmail API."
    message = create_message(sender, to, subject, message_text)
    send_message(service, "me", message)

if __name__ == '__main__':
    main()
