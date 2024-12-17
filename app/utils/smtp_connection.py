'''
# smtp_client.py
from builtins import Exception, int, str
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.config import settings
import logging

class SMTPClient:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, subject: str, html_content: str, recipient: str):
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.username
            message['To'] = recipient
            message.attach(MIMEText(html_content, 'html'))

            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()  # Use TLS
                server.login(self.username, self.password)
                server.sendmail(self.username, recipient, message.as_string())
            logging.info(f"Email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise
'''
# smtp_client.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.config import settings
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

class SMTPClient:
    def __init__(self, server: str = None, port: int = None, username: str = None, password: str = None):
        self.server = server or os.getenv('SMTP_SERVER', settings.smtp_server)
        self.port = port or int(os.getenv('SMTP_PORT', settings.smtp_port))
        self.username = username or os.getenv('SMTP_USERNAME', settings.smtp_username)
        self.password = password or os.getenv('SMTP_PASSWORD', settings.smtp_password)

    def send_email(self, subject: str, html_content: str, recipient: str):
        try:
            # Create the email message
            email_message = MIMEMultipart('alternative')
            email_message['Subject'] = subject
            email_message['From'] = self.username
            email_message['To'] = recipient
            email_message.attach(MIMEText(html_content, 'html'))

            # Connect securely to the SMTP server
            with smtplib.SMTP(self.server, self.port, timeout=10) as server:
                server.set_debuglevel(0)  # Turn off debugging output, can be enabled as needed
                server.starttls()  # Use TLS to upgrade the connection
                server.login(self.username, self.password)
                server.sendmail(self.username, recipient, email_message.as_string())
                logging.info(f"Email successfully sent to {recipient}")
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error occurred while sending email to {recipient}: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error occurred while sending email: {str(e)}")
            raise
