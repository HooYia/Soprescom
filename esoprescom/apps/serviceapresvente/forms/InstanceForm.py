from django import forms
from apps.serviceapresvente.models.Instance import Instance
from apps.serviceapresvente.models.Client_sav import Client_sav
from apps.serviceapresvente.models.Personnels import Personnels

class InstanceForm(forms.ModelForm):
    STATUS=[("En cour","En cour"),
          ("Recouvrement","Recouvrement"),
          ("Décision DG","Décision DG"),
          ("Résolu","Résolu"),
          ("Non résolu","Non résolu")]
    statut = forms.ChoiceField(choices=STATUS,
                                 widget=forms.Select(attrs={'class': 'form-control custom-text-input',
                                                             'id': 'id_instance_statut',
                                                             }),
    )       
    TYPE_INSTANCE=[("Interne","Interne"),
                   ("Externe","Externe")]
    type_instance = forms.ChoiceField(choices=TYPE_INSTANCE,
                                 widget=forms.RadioSelect(attrs={'class': 'custom-radio-input',
                                                             'id': 'id_type_instance'}),
                                  initial="Interne"
    )  
    client = forms.ModelChoiceField(queryset=Client_sav.objects.all(),
                   widget=forms.Select(attrs={'class': 'form-control custom-text-input',}),
                   )   
    responsable = forms.ModelChoiceField(queryset=Personnels.objects.all(),
                   widget=forms.Select(attrs={'class': 'form-control custom-text-input',}),
                   )  
    class Meta:
        model = Instance
        fields = ('idinstance', 'type_instance', 'client', 'numero_dossier','besoin', 'action','responsable',  'statut', 'is_facturable','rapport_technique')

        widgets = {
            #'client' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'numero_dossier' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'besoin' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'action' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
            
            'rapport_technique' : forms.ClearableFileInput(attrs={'class': 'form-control custom-text-input'}),
            'is_facturable' : forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                         'id':'id_is_facturable'}),
     }
