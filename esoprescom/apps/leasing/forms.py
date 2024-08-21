from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.forms import ModelForm
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset,Row, \
                                Column,Submit,HTML,Field
from crispy_forms.bootstrap import TabHolder,Tab
from crispy_forms.bootstrap import FormActions
from django.forms import inlineformset_factory,modelformset_factory


from .models import Clientleasing,Listeimprimante,Deploiement,Consommable,Exploitation, ConsommableExploitation,typeCategorie,typeProduit

class ClientleasingForm(forms.ModelForm):
    class Meta:
        model = Clientleasing
        fields = ('nom', 'adresse', 'contact', 'localite', 'refcontrat', 'email', 'date')

    nom = forms.CharField(label=_('Nom'))
    adresse = forms.CharField(label=_('Adresse'))
    contact = forms.CharField(label=_('Contact'))
    localite = forms.CharField(label=_('Région'))
    refcontrat = forms.CharField(label=_('N° Contrat'))
    email = forms.EmailField(label=_('Email'))
    date = forms.DateField(label=_('Date Contrat'),
                           widget=forms.DateInput(
                                attrs={'type': 'date',
                                'max':datetime.now().date()}))
    

class ListeimprimanteForm(forms.ModelForm):
    class Meta:
        model = Listeimprimante
        exclude= ['userLog']
    date_acquisition = forms.DateField(
              widget=forms.DateInput(
                  attrs={'type': 'date',
                          'max':datetime.now().date()})) 
    endoflife = forms.DateField(
              widget=forms.DateInput(
                  attrs={'type': 'date',
                          'max':datetime.now().date()})) 

class DeploiementForm(forms.ModelForm):
    class Meta:
        model = Deploiement
        exclude= ['userLog']
        #fields = '__all__'
        #fields = ['site', 'adresseip', 'date_deploiement', 'clientleasing', 'listeimprimante']
    date_deploiement = forms.DateField(
              widget=forms.DateInput(
                  attrs={'type': 'date',
                          'max':datetime.now().date()}))    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les imprimantes avec flag=0
        self.fields['listeimprimante'].queryset = Listeimprimante.objects.filter(flag=False)



class ConsommableForm(forms.ModelForm):
      class Meta:
        model = Consommable
        exclude= ['userLog']
        #fields = "__all__"
        widgets = {'categorieproduit': forms.Select(attrs={'class': 'form-control'}), 
                   'typeproduit': forms.Select(attrs={'class': 'form-control', 'id': 'id_typeproduit'}),
                    'modele': forms.Select(attrs={'class': 'form-control', 'id': 'id_modele'}),}
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les imprimantes avec flag=0
        modele_choices = Listeimprimante.objects.filter(flag=0).values_list('designation', flat=True)
        self.fields['modele'] = forms.ChoiceField(
            choices=[(choice, choice) for choice in modele_choices],
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_modele'}),
        )

"""   
class ExploitationForm(ModelForm):
    class Meta:
        model = Exploitation
        exclude= ['userLog']
        #fields = "__all__"
        #fields = ['intervention','deploiement','consommable','quantite','pourcentage_toner',
        #      'ancien_index','nouvel_index','description']
"""

class ConsommableExploitationForm(forms.ModelForm):
    class Meta:
        model = ConsommableExploitation
        fields = ['consommable', 'quantite']

class ExploitationForm(forms.ModelForm):
    class Meta:
        model = Exploitation
        exclude = ['date_exploitation','consommables']  # Exclure le champ non-éditable
        #fields = ['date_exploitation', 'intervention', 'deploiement', 'pourcentage_toner', 'ancien_index', 'nouvel_index']

ConsommableExploitationFormset = inlineformset_factory(
    Exploitation,
    ConsommableExploitation,
    form=ConsommableExploitationForm,
    extra=1,
    can_delete=True)
