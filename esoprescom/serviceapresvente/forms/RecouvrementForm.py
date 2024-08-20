from django import forms
from serviceapresvente.models.Recouvrement import Recouvrement

class RecouvrementForm(forms.ModelForm):
    ETAT=[("Sav payé","Sav payé"), 
          ("Sav non payé","Sav non payé")] 
    
      
    #statut = forms.ChoiceField(choices=ETAT,
    #                           widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
    #                                                          'id':'id_recouvrementstatut',
    #                                                          'name':'statut'}),
    #                            initial= 'Sav non payé'
    #)  
    class Meta:
        model = Recouvrement
        fields = ('livraisonclient','is_devea_request','statut','facture_client','montant_client', 'commentaire')

        widgets = {
            'livraisonclient' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_livraisonclient'}),
            'montant_client' : forms.NumberInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_montant_client'}),
            'is_devea_request' : forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                           'id':'id_is_devea_request',
                                                            'disabled':'disabled'}),   
            'statut' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 
                                                       'id':'id_statut'}), 
            'facture_client' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
                                                                     'id': 'id_facture_client'}),
            'commentaire' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
        }
