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


from .models import Clientleasing,Listeimprimante,Deploiement,Consommable,Exploitation, ConsommableExploitation

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
        exclude= ['flag']
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
        fields = "__all__"
        quantite = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '1'}))
        seuilLimite = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '5'}))
        #updated_at = forms.DateField(
        #      widget=forms.DateInput( attrs={'type': 'date', }))   
        # Afficher uniquement les modèles distincts dans le formulaire
        modeleimprimante = forms.ModelChoiceField(
            queryset=Listeimprimante.objects.values_list('reference',).distinct(),
            to_field_name="reference",
            required=True,
            label="Modèle Imprimante"
        )
        widgets = {'modele': forms.Select(attrs={'class': 'form-control',
                                                 'id': 'id_modele'}), 
                   'produit': forms.Select(attrs={'class': 'form-control',
                                                   'id': 'id_typeproduit'}),
                   'reference' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
                   'designation' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
                   'description' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
                   'updated_at'   :forms.DateInput( attrs={'type': 'date', }),
                   #'quantite' : forms.NumberInput(attrs={'min': '0'}),
                   #'seuilLimite' : forms.NumberInput(attrs={'min': '5'}),
                   }
        def clean(self):
            cleaned_data = super().clean()
            produit = cleaned_data.get('produit')

            # Si le produit est du PAPIER, on enlève l'obligation de choisir un modèle
            if produit == Consommable.TYPE_PRODUIT.PAPIER:
                cleaned_data['modeleimprimante'] = None
            else:
                # Si ce n'est pas du papier, on impose la présence du modèle d'imprimante
                if not cleaned_data.get('modeleimprimante'):
                    self.add_error('modeleimprimante', 'Veuillez sélectionner un modèle d\'imprimante.')

            return cleaned_data
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les imprimantes avec flag=0
        modele_choices = Listeimprimante.objects.filter(flag=0).values_list('designation', flat=True)
        self.fields['modele'] = forms.ChoiceField(
            choices=[(choice, choice) for choice in modele_choices],
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_modele'}),
        )

    """   

"""
class ExploitationForm(ModelForm):
    class Meta:
        model = Exploitation
        fields = "__all__"
        #fields = ['intervention','deploiement','consommable','quantite','pourcentage_toner',
        #      'ancien_index','nouvel_index','description']
"""

class ConsommableExploitationForm(forms.ModelForm):
    consommable = forms.ModelMultipleChoiceField(
        queryset=Consommable.objects.all(),  
        widget=forms.SelectMultiple(
            attrs={
                'style': 'width: 50%;', 
                'class': 'form-control'  
            }
        ),
        label="Consommable"  
    )

    class Meta:
        model = ConsommableExploitation
        fields = ['consommable', 'quantite']  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Utilisation de la désignation au lieu de l'ID
        self.fields['consommable'].label_from_instance = lambda obj: f"{obj.designation} ({obj.reference})"    

class ExploitationForm(forms.ModelForm):
    class Meta:
        model = Exploitation
        fields = "__all__"
        #fields = ['date_exploitation', 'intervention', 'deploiement', 'pourcentage_toner', 'ancien_index', 'nouvel_index']

ConsommableExploitationFormset = inlineformset_factory(
    Exploitation,
    ConsommableExploitation,
    form=ConsommableExploitationForm,
    extra=1,
    can_delete=True)
