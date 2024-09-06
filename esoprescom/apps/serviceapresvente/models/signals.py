from .models import Sav_request,Sav_test_request
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .tasks import Send_Email
import logging

logger = logging.getLogger(__name__)

#@receiver(post_save, sender=Sav_test_request)
@receiver(post_save, sender=Sav_request)
def send_email_on_sav_request_created(sender, instance, created, **kwargs):
    if created:  # Vérifie si une nouvelle instance a été créée
        subject = 'Nouvelle requête SAV créée'
        #client_email = instance.client_sav.email
        client_email = 'donsetogola@gmail.com'
        message = f"Une nouvelle requête SAV a été créée avec le numéro de dossier : {instance.numero_dossier}"
        from_email = 'souleymane@soprescom.net'
        to_email = [client_email]  # Liste des destinataires
        send_mail(subject, message, from_email, to_email,fail_silently=False)
        try:
            Send_Email(subject, message, from_email, to_email)
            logger.info(f"Email envoyé à {client_email} pour la nouvelle requête SAV.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {client_email}: {str(e)}")


@receiver(post_save, sender=Sav_request)
def send_email_on_receptionPiece(sender, instance, created, **kwargs):
    if instance.status == 'Phase4_terminer':
        subject = 'Livraison de la requête SAV'
        message = f"La requête SAV avec le numéro de dossier {instance.numero_dossier} est prête pour la livraison. "
        from_email = 'your@email.com'
        to_email = ['livraison1@email.com', 'livraison2@email.com']
        send_mail(subject, message, from_email, to_email)

@receiver(post_save, sender=Sav_request)
def send_email_on_livraison(sender, instance, created, **kwargs):
    if instance.status == 'Phase4_terminer':
        subject = 'Livraison de la requête SAV'
        message = f"La requête SAV avec le numéro de dossier {instance.numero_dossier} est prête pour la livraison. "
        from_email = 'your@email.com'
        to_email = ['livraison1@email.com', 'livraison2@email.com']
        send_mail(subject, message, from_email, to_email)

              
@receiver(post_save, sender=Sav_request)
def send_email_on_recouvrement(sender, instance, created, **kwargs):
    if instance.status == 'Phase3_validationdevis':
        subject = 'Validation du devis pour la requête SAV'
        message = f"La requête SAV avec le numéro de dossier {instance.numero_dossier} a été validée. "
        from_email = 'your@email.com'
        to_email = ['recouvrement1@email.com', 'recouvrement2@email.com']
        send_mail(subject, message, from_email, to_email)