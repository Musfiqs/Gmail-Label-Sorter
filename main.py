import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from gmail_handler import GmailHandler
from email_classifier import EmailClassifier
import config

def process_emails(gmail_handler: GmailHandler, classifier: EmailClassifier, test_mode: bool = False):
    """Process emails and apply labels."""
    print("Fetching recent emails...")
    emails = gmail_handler.get_recent_emails()
    print(f"Found {len(emails)} emails to process")
    
    for email in emails:
        label = classifier.classify_email(email)
        email_id = email['id']
        
        # Skip emails that don't match any category (label is None)
        if label is None:
            print(f"Email {email_id} - No category match, skipping labeling")
            continue
        
        if test_mode:
            print(f"Would label email {email_id} as: {label}")
        else:
            if gmail_handler.apply_label(email_id, label):
                logging.info(f"Successfully labeled email {email_id} as {label}")
                print(f"Email labeled as: {label}")
            else:
                logging.error(f"Failed to label email {email_id}")

def main():
    print("Starting Gmail Labeler...")
    try:
        print("Authenticating with Gmail...")
        gmail_handler = GmailHandler()
        classifier = EmailClassifier()
        
        print("Processing existing emails...")
        process_emails(gmail_handler, classifier)
        
        print("Setting up background scheduler...")
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            process_emails,
            'interval',
            seconds=config.CHECK_INTERVAL,
            args=[gmail_handler, classifier]
        )
        
        scheduler.start()
        print(f"Scheduler started. Checking for new emails every {config.CHECK_INTERVAL} seconds.")
        print("Press Ctrl+C to exit")
        
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Error in main: {str(e)}")
        raise
    except KeyboardInterrupt:
        print("\nShutting down...")
        scheduler.shutdown()

if __name__ == '__main__':
    main() 