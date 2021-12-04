from dotenv import load_dotenv
load_dotenv()
import smtplib
import os


email_gmail = os.environ.get("email_gmail")
pwd_gmail = os.environ.get("pwd_gmail")


def send_email(user, email):
    message_to_send = f"Subject:Approbation - nouveau bénévole: {user.username} \n\nUn bénévole a demandé à" \
                      f" être dans votre site. Merci de valider cet utilisateur: {user.username}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email_gmail, password=pwd_gmail)
        connection.sendmail(from_addr=email_gmail, to_addrs=email, msg=message_to_send.encode('utf-8'))

from django.core import mail

# emails = (
#     ('Hey Man', "I'm The Dude! So that's what you call me.", 'dude@aol.com', ['mr@lebowski.com']),
#     ('Dammit Walter', "Let's go bowlin'.", 'dude@aol.com', ['wsobchak@vfw.org']),
# )
# results = mail.send_mass_mail(emails)


# TRY THIS ONE
# https://pypi.org/project/django-celery-email/

#OR
# https://github.com/ui/django-post_office
# https://pythonrepo.com/repo/ui-django-post_office--python-sending-and-parsing-email

# OR
# https://medium.com/@EmadMokhtar/send-emails-asynchronously-from-django-3c1e41b526c3


# OR
# import threading
# from threading import Thread
#
# class EmailThread(threading.Thread):
#     def __init__(self, subject, html_content, recipient_list):
#         self.subject = subject
#         self.recipient_list = recipient_list
#         self.html_content = html_content
#         threading.Thread.__init__(self)
#
#     def run (self):
#         msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
#         msg.content_subtype = "html"
#         msg.send()
#
# def send_html_mail(subject, html_content, recipient_list):
#     EmailThread(subject, html_content, recipient_list).start()

#OR


# from django.core.mail import send_mail as core_send_mail
# from django.core.mail import EmailMultiAlternatives
# import threading
#
# class EmailThread(threading.Thread):
#     def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
#         self.subject = subject
#         self.body = body
#         self.recipient_list = recipient_list
#         self.from_email = from_email
#         self.fail_silently = fail_silently
#         self.html = html
#         threading.Thread.__init__(self)
#
#     def run (self):
#         msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
#         if self.html:
#             msg.attach_alternative(self.html, "text/html")
#         msg.send(self.fail_silently)
#
# def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
#     EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()