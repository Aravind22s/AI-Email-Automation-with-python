def build_email_context(email):
    context = f"""
    Sender Name: {email["sender_name"]}
    Sender Email: {email["sender_email"]}
    Subject: {email["subject"]}
    Date: {email["date"]}
    Has Attachment: {email["has_attachment"]}
    Email_body: {email["body"]}"""
    
    return context.strip()