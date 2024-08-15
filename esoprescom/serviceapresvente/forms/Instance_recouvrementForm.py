from django import forms
from serviceapresvente.models.Instance_recouvrement import Instance_recouvrement

class Instance_recouvrementForm(forms.ModelForm):
    FACTURE_ETAT= [("Payé","Payé"),
                   ("Non Payé","Non Payé")]
    facture_statut = forms.ChoiceField(choices=FACTURE_ETAT,
                                 widget=forms.RadioSelect(attrs={'class': 'custom-radio-input',
                                                             'id': 'id_type_SAV'}),
                                 initial="Non Payé"
    )     
    class Meta:
        model = Instance_recouvrement
        fields = ('idrecouv', 'instance', 'facture_reference', 'facture_montant', 'facture_statut')

        widgets = {
             'instance' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_instance'}),
            'facture_reference' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'facture_montant' : forms.NumberInput(attrs={'class': 'form-control custom-float-input'}),
            #'facture_statut' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            }
