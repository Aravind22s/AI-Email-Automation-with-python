from gmail_services import (get_unread_emails, 
                            get_email_details,
                            extract_email_data)
from ai_service import generate_reply

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
    
        print("=" * 50)
        print("AI GENERATED REPLY")
        print("=" * 50)
        
        result = generate_reply(data)
        
        print("CATEGORY")
        print(result["category"])
        print("=" * 50)
        
        print("AI REPLY")
        print(result["reply"])
        print("=" * 50)



        
if __name__ == "__main__":
    main()