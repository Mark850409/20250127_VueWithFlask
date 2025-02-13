from flask_mail import Message,Mail
from flask import current_app
from factory import create_app

app = create_app()
mail = Mail()

def test_email():
    msg = Message('Test Subject',
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],
                    recipients=['test@example.com'])
    msg.body = "This is a test email."
    mail.send(msg)

if __name__ == '__main__':
    with current_app.app_context():
        test_email()