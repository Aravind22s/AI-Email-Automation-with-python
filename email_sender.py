import base64
from email.mime.text import MIMEText
from gmail_services import get_service

def create_message(sender, to, subject, body, thread_id):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = f"Re: {subject}"
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {
        'raw': raw_message,
        'threadId': thread_id}

def send_email(sender, reciver, subject, body, thread_id):
    service = get_service()
    message = create_message(sender, reciver, subject, body, thread_id)
    sent_message = service.users().messages().send(userId='me', body=message).execute()
    return sent_message