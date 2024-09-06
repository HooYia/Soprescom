from django import forms
from datetime import datetime
from django.utils.translation import gettext_lazy as _

from apps.leasing.models.Client import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('idclientleasing', 'nom', 'adresse', 'contact', 'localite', 'refcontrat', 'email', 'date',)

        widgets = {
            'nom' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'adresse' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'contact' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'localite' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'refcontrat' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control custom-email-input'}),
            #'date' : forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }
    
        date = forms.DateField(label=_('Date Contrat'),
                           widget=forms.DateInput(
                                attrs={'type': 'date',
                                'max':datetime.now().date()}))