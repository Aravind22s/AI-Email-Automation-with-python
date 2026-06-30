from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from email.utils import parseaddr
import base64
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "config", "token.json")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "config", "credentials.json")

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def authenticate():
    creds = None
    
    #load existing token
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        print
        
    #if token is missing or expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "CREDENTIALS_PATH",
                SCOPES)
            creds = flow.run_local_server(port=0)
        
            #save token
            with open("TOKEN_PATH", "w") as token:
                token.write(creds.to_json())
    return creds

def get_service():
    creds = authenticate()
    service = build("gmail","v1",credentials=creds)
    return service

def get_unread_emails():
    service = get_service()
    results = service.users().messages().list(
        userId = "me",
        labelIds = ["INBOX"],
        q = "is:unread"
    ).execute()
    messages = results.get("messages", [])
    return messages

def get_email_details(message_id):
    service = get_service()
    message = service.users().messages().get(
        userId = "me",
        id = message_id,
        format = "full"
    ).execute()
    return message

def decode_base64(data):
    data = data.replace("-", "+") 
    data = data.replace("_", "/")
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return base64.urlsafe_b64decode(data).decode("utf-8",errors="ignore")

def clean_html(html):
    soup = BeautifulSoup(html,"html.parser")
    return soup.get_text(separator="\n", strip=True)

def extract_sender(sender):
    name, email = parseaddr(sender)
    # If sender has no display name,
    # use the first part of the email.
    if not name:
        if "@" in email:
            name = email.split("@")[0]
        else:
            name = "Unknown"
    return {
        "name": name,
        "email": email}
    
def has_attachment(payload):
    parts = payload.get("parts",[])
    for part in parts:
        filename = part.get("filename","")
        if filename:
            return True
        if part.get("parts"):
            if has_attachment(part):
                return True
    return False

def get_email_body(payload):
    # Case 1: Email body exists directly
    body = payload.get("body", {})
    if body.get("data"):
        return decode_base64(body["data"])

    # Case 2: Email has multiple parts
    parts = payload.get("parts", [])
    for part in parts:
        mime_type = part.get("mimeType")
        # Plain text email
        if mime_type == "text/plain":
            data = part.get("body",{}).get("data")
            if data:
                return decode_base64(data)
        # HTML email
        if mime_type == "text/html":
            data = part.get("body",{}).get("data")
            if data:
                html = decode_base64(data)
                return clean_html(html)
        # Nested multipart
        if part.get("parts"):
            nested = get_email_body(part)
            if nested:
                return nested
    return ""

def extract_email_data(message):
    payload = message.get("payload",{})
    headers = payload.get("headers",[])
    subject = "No Subject"
    sender = "Unknown"
    date = ""
    for header in headers:
        header_name = header.get("name")
        header_value = header.get("value")
        if header_name == "Subject":
            subject = header_value
        elif header_name == "From":
            sender = header_value
        elif header_name == "Date":
            date = header_value
    sender_info = extract_sender(sender)
    body = get_email_body(payload)
    return {
        "message_id": message.get("id"),
        "thread_id": message.get("threadId"),
        "sender_name": sender_info["name"],
        "sender_email": sender_info["email"],
        "subject": subject,
        "date": date,
        "body": body,
        "has_attachment": has_attachment(payload)}