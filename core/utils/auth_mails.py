from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class Util:
    @staticmethod
    def send_registration_mail(data):
        html_content = render_to_string(
            "auth_mails/registration_mail.html",
            {"absurl": data["absurl"]}
        )
        msg = EmailMessage(
            subject="Registration Mail", body=html_content,
            to=[data["to_email"]]
        )
        msg.content_subtype = "html"
        msg.send()
