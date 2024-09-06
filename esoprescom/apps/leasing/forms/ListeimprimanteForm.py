from django import forms
from datetime import datetime
from apps.leasing.models.Listeimprimante import Listeimprimante

class ListeimprimanteForm(forms.ModelForm):
    class Meta:
        model = Listeimprimante
        fields = ('idlisteimprimante', 'numero_serie', 'reference', 'designation', 'description', 'date_acquisition', 'garantie', 'endoflife')

        widgets = {
            'numero_serie' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'reference' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'designation' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'description' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            #'date_acquisition' : forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'garantie' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            #'endoflife' : forms.DateInput(attrs={'class': 'form-control datepicker'}),
           
        }
    date_acquisition = forms.DateField(
              widget=forms.DateInput(
                  attrs={'type': 'date',
                          'max':datetime.now().date()})) 
    endoflife = forms.DateField(
              widget=forms.DateInput(
                  attrs={'type': 'date',
                          'max':datetime.now().date()}))    
