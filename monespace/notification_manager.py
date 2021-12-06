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
