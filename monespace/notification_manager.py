import smtplib
import os
import environ
from django.core.mail import send_mail, send_mass_mail

env = environ.Env()
# reading .env file
environ.Env.read_env()

email_gmail = env("email_gmail")
pwd_gmail = env("pwd_gmail")


def send_email(type_email, to_user, from_user):
    # print(to_user)
    if type_email == 1:
        subject = f"Approbation d'un nouveau bénévole"
        message_body = f"Un bénévole a demandé à être bénévole dans votre site. Merci d'approuver ou non cet utilisateur depuis la plateforme."
    elif type_email == 2:
        subject = f"Nouveau message pour vous sur la plateforme des bénévoles"
        message_body = "Vous venez de recevoir un nouveau message. Merci de vous connecter à la plateforme."
    elif type_email == 3:
        subject = f"Votre approbation pour rejoindre la distribution a été acceptée"
        message_body = "Vous venez d'être approuvé par le responsable de distribution. Vous pouvez maintenant vous rendre sur la plateforme et indiquer vos présences / voir les communications."
    elif type_email == 4:
        subject = f"Votre demande pour rejoindre la distribution a été refusée"
        message_body = "Si vous pensez que cela pourrait être une erreur, merci de communiquer avec nous."
    elif type_email == 5:
        subject = f"Une distribution dans 2 jours!"
        message_body = "Ceci est un rappel que vous êtes présent pour une distribution dans 2 jours. Merci de modifier votre présence si jamais vous ne pouvez malheureusement plus venir."
    else:
        subject = 'Notification de la plateforme des bénévoles'
        message_body = 'Merci de vous connecter à la plateforme.'

    emails_pre = []
    for i in to_user:
        if i != from_user:
            # print(i)
            email = (subject, message_body, email_gmail, [i.email])
            emails_pre.append(email)
    emails = tuple(emails_pre)
    send_mass_mail(emails)

    # try:
    #     send_mass_mail(emails)
    # except:
    #     print('error')

    # send_mail(
    # subject,
    # message_body,
    # email_gmail,
    # [to_user.email],
    # fail_silently=False,)


# emails = (
#     ('Hey Man', "I'm The Dude! So that's what you call me.", 'dude@aol.com', ['mr@lebowski.com']),
#     ('Dammit Walter', "Let's go bowlin'.", 'dude@aol.com', ['wsobchak@vfw.org']),
# )
# results = mail.send_mass_mail(emails)
