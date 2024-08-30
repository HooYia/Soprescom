
import json
import logging
import requests
from typing import Any, Dict, List, Optional

from django.conf import settings
from config.celery import app
from django.template.loader import render_to_string

from django.utils.translation import gettext_lazy as _


from django.conf import settings


from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

logger = logging.getLogger(__name__)

            
class EmailUtil(object):
    def __init__(self) -> None:
        
        self.prod = True         
        
    def send_generic_email(self, subject: str, content: str, to: list, _from: str = None) -> bool:
        logger.info("## Sending generic email ##")
      
        
        if not self.prod:
            subject = "{TEST} " + subject
            
       
           
        else:
            try:
                logger.info(f"Email subject: {subject}")

                # Using Django's send_mail
                # send_mail(
                #     subject,
                #     content,
                #     _from or f"<{settings.ADMIN_EMAIL}>",
                #     [to],
                #     fail_silently=False,
                #     html_message=content,
                # )

                #Alternatively, using EmailMessage
                
                email = EmailMessage(
                    subject,
                    content,
                    _from or f"gps-shopping.com <{settings.EMAIL_HOST_USER}>",
                   to,
                )
                email.content_subtype = "html"
                email.send()

                logger.info("Generic email sent successfully.")
                return True
            except Exception as e:
                logger.error(f"Exception: {e}")   
                return False
                
                
    @app.task            
    def send_email_with_template(self, template: str, context:dict, recievers:list, subject:str) -> bool:
        """ send email with template """
        
        context['subject'] = subject
        body = render_to_string(
            template_name=template,
            context=context
        )
        
        try:
            sent = self.send_generic_email(
                subject=subject,
                content=body,
                to=recievers
            )
            if sent:
                return True
            else:
                return False
        except Exception as e:
            logger.info(f"An error occurred: {e}") 
            return False            