import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask import url_for, render_template

load_dotenv()
mail = Mail()


def send_confirmation_email(user_email) -> None:
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    confirm_url = url_for(
        "confirm_email",
        token=serializer.dump(user_email, salt="email-confirmation-salt"),
        _extermal=True
    )
    html = render_template("admin/templates/email_confirmation.html", confirm_url=confirm_url)
    message = Message(
        "Confirm Email Address",
        recipients=[],
        sender=("Flask Shop 7 GROUP", os.getenv("EMAIL")),
        html=html
    )
    mail.send(message)
