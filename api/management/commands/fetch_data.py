from django.core.management.base import BaseCommand
from api.models import JobApplication
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
from api.utils.decrypt import load_credentials  # Updated import statement

class Command(BaseCommand):
    help = 'Fetch job application details from email and store in the database'

    def handle(self, *args, **kwargs):
        # Fetch the credentials using load_credentials
        try:
            email_address, app_password = load_credentials()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading credentials: {e}"))
            return
        
        # Connect to the Gmail IMAP server
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_address, app_password)
            mail.select('inbox')
            self.stdout.write(self.style.SUCCESS('Successfully logged in to the email account.'))
        except imaplib.IMAP4.error as e:
            self.stdout.write(self.style.ERROR(f"Failed to login: {e}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
            return

        # Search for all emails
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()

        # Iterate over the email IDs
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Decode email subject
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            # Get email content
            body = self.get_email_body(msg)

            # Process the email content
            organization = self.extract_organization(body)
            designation = self.extract_designation(body)
            job_location = self.extract_location(body)
            date_of_application = self.extract_date(body)

            # Convert email date to IST
            time_of_application = msg['Date']
            time_of_application = email.utils.parsedate_to_datetime(time_of_application)
            time_of_application = time_of_application.astimezone(pytz.timezone('Asia/Kolkata'))

            # Save data to JobApplication model
            JobApplication.objects.create(
                organization=organization,
                job_location=job_location,
                date_of_application=date_of_application,
                time_of_application=time_of_application,
                designation=designation
            )

        mail.logout()

    def get_email_body(self, msg):
        """Extracts and returns the body from an email message."""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                if 'attachment' not in content_disposition and content_type in ['text/plain', 'text/html']:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors='ignore')
                        if content_type == 'text/html':
                            soup = BeautifulSoup(body, 'html.parser')
                            return soup.get_text()
                        else:
                            return body
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                return payload.decode(errors='ignore')
        return ""

    def extract_organization(self, body):
        # Your logic to extract organization from the email body
        pass

    def extract_designation(self, body):
        # Your logic to extract designation from the email body
        pass

    def extract_location(self, body):
        # Your logic to extract location from the email body
        pass

    def extract_date(self, body):
        # Your logic to extract the date from the email body
        pass
