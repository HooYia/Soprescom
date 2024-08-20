from django import forms
from serviceapresvente.models.LivraisonClient import LivraisonClient

class LivraisonForm(forms.ModelForm):
    ETAT=[("Sav livré","Sav livré"), 
          ("Sav non livré","Sav non livré")] 
      
    #statut = forms.ChoiceField(choices=ETAT,
    #                               widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
    #                                                          'id':'id_statut',
    #                                                          'name':'statut'}), 
    #                               initial='Sav non livré'
    #)  
    class Meta:
        model = LivraisonClient
        fields = ('assamblagereparation', 'statut','bordereau_livraison','commentaire')

        widgets = {
            'assamblagereparation' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_assamblagereparation'}),
            'statut' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 
                                                       'id':'id_statut'}), 
            'bordereau_livraison' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
                                                                 'id': 'id_bordereau_livraison',
                                                                 }),
            'commentaire' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
        }
