from gmail_services import (get_unread_emails, 
                            get_email_details,
                            extract_email_data,
                            mark_as_read,
                            add_label,
                            already_replied)
from ai_service import generate_reply
from email_sender import send_email
from logger import save_email_log, is_processed

def main():
    
    emails = get_unread_emails()
    
    if not emails:
        print("No unread email found.")
        return
    
    print(f"\nfound {len(emails)} unread emails\n")
    
    for index, email in enumerate(emails, start=1):
        print("="*50)
        print(f"Email {index}")
        print("="*50)
        
        message = get_email_details(email["id"])
        data = extract_email_data(message)

        print("MESSAGE ID")
        print(data["message_id"])
        
        print("\nTHREAD ID")
        print(data["thread_id"])
    
        print("\nSENDER NAME")
        print(data["sender_name"])
    
        print("\nSENDER EMAIL")
        print(data["sender_email"])
    
        print("\nDATE")
        print(data["date"])
    
        print("\nSUBJECT")
        print(data["subject"])
    
        print("\nHAS ATTACHMENT")
        print(data["has_attachment"])
    
        print("\nEMAIL BODY")
        print(data["body"])
    
        print("\nALREADY REPLIED")
        if already_replied(message):
            print("Already replied to this email. Skipping...")
            continue
        
        if is_processed(data["message_id"]):
            print("This email has already been processed. Skipping...")
            continue
        
        print("=" * 50)
        print("AI GENERATED REPLY")
        print("=" * 50)
        
        try:
            result = generate_reply(data)
        except Exception as e:
            print(f"Error generating reply: {e}")
            save_email_log(
                data["message_id"],
                data["sender_email"],
                data["subject"],
                "AI Reply Generation Failed" 
            ) 
            continue
        
        choice = input("Do you want to send the reply? (y/n): ")
        
        if choice.lower() == 'y':
            try:
                sent_message = send_email(
                    sender=data["sender_email"],
                    reciver=data["sender_email"],
                    subject=data["subject"],
                    body=result["reply"],
                    thread_id=data["thread_id"]
                )
                print(f"Reply sent successfully! Message ID: {sent_message['id']}")
            except Exception as e:
                print(f"Error sending email: {e}")
                save_email_log(
                    data["message_id"],
                    data["sender_email"],
                    data["subject"],
                    "Email Sending Failed" 
                ) 
                continue
        else:
            print("Reply Cancelled.")
        
        print("CATEGORY")
        print(result["category"])
        print("=" * 50)
        
        print("AI REPLY")
        print(result["reply"])
        print("=" * 50)

        mark_as_read(data["message_id"])
        add_label(data["message_id"], "AI Replied")
        print("Email marked as read and labeled as 'AI Replied'.")
        
        save_email_log(
            data["message_id"],
            data["sender_email"],
            data["subject"],
            "Replied" 
        )    
        
if __name__ == "__main__":
    main()