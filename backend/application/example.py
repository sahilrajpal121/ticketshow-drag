import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER_HOST = '127.0.0.1'
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "email@sahil.com"
SENDER_PASSWORD = 'password'

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg['From'] = "email@sahil.com"
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    # s = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    # s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s = smtplib.SMTP('127.0.0.1', 1025)
    s.login("email@sahil.com", "password")
    s.send_message(msg)
    s.quit()

    return True

def main():
    new_users = [
        { "name": "Sahil", "email": "test@example.com"},
        { "name": "something", "email": "something@example.com"}
    ]

    for user in new_users:
        send_email(user['email'], 'Welcome to the app', f"Hi {user['name']}, welcome to the app")

if __name__ == "__main__":
    main()
