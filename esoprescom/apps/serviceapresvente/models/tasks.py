
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage,BadHeaderError
from config.celery import app 
from celery import  shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

#from essaiedjango.celery import app

def Send_Email(subject, message, from_email, to_email):
    """
    Fonction pour envoyer un e-mail en utilisant smtplib.
    """
    smtp_server = 'ssl0.ovh.net' # 'ssl0.ovh.net' #  'proX.mail.ovh.net'
    smtp_port = 587  # Port SMTP pour TLS

    sender_email = from_email
    receiver_email = to_email
    password = 'Donse@2000'  # Vous devrez sécuriser le stockage du mot de passe
    # Création du message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        # Connexion au serveur SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Activation du mode TLS
            server.login(sender_email, password)  # Authentification SMTP
            
            # Envoi de l'e-mail
            server.sendmail(sender_email, receiver_email, msg.as_string())
            
            print("Email sent successfully!")
    except BadHeaderError as e:
        print('Erreur d\'entête de mail :', e)
    except Exception as e:
        print('Erreur lors de l\'envoi du mail :', e)



def send_email_with_template_v2(subject, template_name,context,to_email:list, from_email):
    """
    Fonction pour envoyer un e-mail en utilisant smtplib.
    """
    try:
        # Création du message
        message = render_to_string(template_name, context)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        
        # Connexion au serveur SMTP
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
        
        print("Second method: Email sent successfully!")
    except Exception as e:
        print('Erreur lors de l\'envoi du mail :', e)




def send_email_with_template(subject,template_name,context,to_email:list,from_email):
    try:
          message = render_to_string(template_name,context)
          email = EmailMessage(subject,message,from_email,to_email)
          email.send()
          print("Second methode: Email sent successfully!")
    except BadHeaderError as e:
          print('Erreur d\'entête de mail :', e)
    except Exception as e:
          print('Erreur lors de l\'envoi du mail :', e)      
    return True

#@shared_task

@app.task
def send_email_with_template_task(subject, template_name,context,to_email:list, from_email):
    """
    Fonction pour envoyer un e-mail en utilisant smtplib.
    """
    try:
        # Création du message
        message = render_to_string(template_name, context)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        
        # Connexion au serveur SMTP
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
         
        print("Second method: Email sent successfully!")
        logger.info("Email sent successfully!")
    except Exception as e:
        print('Erreur lors de l\'envoi du mail :', e)
        logger.error(f"Error sending email: {e}")



@app.task
def send_instance_email_with_template_task(subject, template_name,context,to_email:list, from_email):
    """
    Fonction pour envoyer un e-mail en utilisant smtplib.
    """
    try:
        # Création du message
        message = render_to_string(template_name, context)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        
        # Connexion au serveur SMTP
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
         
        print("Email sent successfully!")
        logger.info("Email sent successfully!")
    except Exception as e:
        print('Erreur lors de l\'envoi du mail :', e)
        logger.error(f"Error sending email: {e}")
        
# def send_generic_email(subject: str, content: str, to: list, _from: str = None) -> bool:
#     logger.info("## Sending generic email ##")
#     try:
#         logger.info(f"Email subject: {subject}")
        
#         email = EmailMessage(
#             subject,
#             content,
#             _from or f"Soprescom <{settings.EMAIL_HOST_USER}>",
#             to,
#         )
#         email.content_subtype = "html"
#         email.send()

#         logger.info("Generic email sent successfully.")
#         return True
#     except Exception as e:
#         logger.error(f"Exception: {e}")   
#         return False
        
        
# @app.task 
# def send_email_with_template(template: str, context:dict, recievers:list, subject:str) -> bool:
#     """ send email with template """
    
#     context['subject'] = subject
#     body = render_to_string(
#         template_name=template,
#         context=context
#     )
    
#     try:
#         sent = send_generic_email(
#             subject=subject,
#             content=body,
#             to=recievers
#         )
#         if sent:
#             return True
#         else:
#             return False
#     except Exception as e:
#         logger.info(f"An error occurred: {e}") 
#         return False   


@app.task
def send_email_with_template_customer(subject, template_name, context, to_email:list, from_email):
    """
    Fonction pour envoyer un e-mail en utilisant smtplib.
    """
    try:
        # Création du message
        message = render_to_string(template_name, context)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        
        # Connexion au serveur SMTP
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
         
        print("Email sent successfully!")
        logger.info("Email sent successfully!")
    except Exception as e:
        print('Erreur lors de l\'envoi du mail :', e)
        logger.error(f"Error sending email: {e}")