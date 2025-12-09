# mail_service.py
import os
import smtplib
from email.message import EmailMessage
from flask import render_template
from debug import ic

MAIL_HOST = os.getenv("MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "1") == "1"
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USER)

def send_email(to_email: str, subject: str, html_body: str):
    ic("Preparing to send email", to_email, subject)

    if not MAIL_USER or not MAIL_PASSWORD:
        ic("MAIL_USER or MAIL_PASSWORD not set - skipping real send")
        ic("EMAIL DEBUG DUMP", html_body)
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = to_email
    msg.set_content("This email requires an HTML-capable email client.")
    msg.add_alternative(html_body, subtype="html")

    try:
        if MAIL_USE_TLS:
            server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)

        server.login(MAIL_USER, MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        ic("Email sent successfully to", to_email)
    except Exception as ex:
        ic("EMAIL SEND ERROR", ex)


def send_verification_email(user_email: str, verification_token: str):
    """
    Sender en email til brugeren med et verify-link.
    """
    ic("send_verification_email called", user_email, verification_token)

   
    verify_url = f"http://localhost:5001/verify/{verification_token}"

    html_body = render_template(
        "partials/emails/_verify_email.html",
        verify_url=verify_url
    )

    send_email(
        to_email=user_email,
        subject="Verify your Socia account",
        html_body=html_body
    )


def send_password_reset_email(user_email: str, reset_token: str):

    """
    Sender en email til brugeren med et password reset-link.
    """
    ic("send_password_reset_email called", user_email, reset_token)

    reset_url = f"http://localhost:5001/reset-password/{reset_token}"

    html_body = render_template(
        "partials/emails/_reset_password.html",
        reset_url=reset_url
    )

    send_email(
        to_email=user_email,
        subject="Reset your Socia password",
        html_body=html_body
    )


def send_user_block_email(user_email: str):
    """
    Sender en email til brugeren, når deres konto bliver blokeret.
    """
    ic("send_user_block_email called", user_email)

    html_body = render_template(
        "partials/emails/user_blocked.html"
    )

    send_email(
        to_email=user_email,
        subject="Your Socia account has been blocked",
        html_body=html_body
    )


def send_post_block_email(user_email: str, post_preview: str | None = None):
    """
    Sender en email til brugeren, når en af deres posts bliver blokeret.
    """
    ic("send_post_block_email called", user_email, post_preview)

    html_body = render_template(
        "partials/emails/post_blocked.html",
        post_preview=post_preview
    )

    send_email(
        to_email=user_email,
        subject="One of your Socia posts has been blocked",
        html_body=html_body
    )