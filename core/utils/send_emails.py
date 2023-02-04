from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_emails(subject, template, context, to_user):
    body = render_to_string(
        template, context
    )
    email = EmailMessage(
        subject=subject, body=body, to=[to_user]
    )
    email.content_subtype = "html"
    email.send()
