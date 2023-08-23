from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .threadings import EmailThreading


def send_emails(subject, template, context, to_user):
    body = render_to_string(
        template, context
    )
    email = EmailMessage(
        subject=subject, body=body, to=[to_user]
    )
    email.content_subtype = "html"
    EmailThreading(email).start()
