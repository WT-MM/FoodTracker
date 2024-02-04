import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create the MIME object
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    # Establish a secure connection with the SMTP server
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, to_email, message.as_string())

# Example usage
if __name__ == "__main__":
    # Replace these with your own email and SMTP server details
    email_subject = "Test Email Notification"
    email_body = "This is a test email notification from your Python script."
    recipient_email = "sebastianhorta03@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "devfest2024@gmail.com"
    smtp_password = "mumr lpyo bvyj ojea"

    send_email(email_subject, email_body, recipient_email, smtp_server, smtp_port, smtp_username, smtp_password)