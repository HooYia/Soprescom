from django import forms
from serviceapresvente.models.CommandeSav import CommandeSav
from serviceapresvente.models.Fournisseurs import Fournisseurs

class CommandeSavForm(forms.ModelForm):
    ETAT=[("commande placée","commande placée"),
          ("pending (achat)","pending (achat)")
        ]    
    #statut = forms.ChoiceField(choices=ETAT,
    #                               widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
    #                                                          'id':'id_statut',
    #                                                          'name':'statut'}), 
    #                               initial = 'pending (achat)'
    #)       
    fournisseur = forms.ModelChoiceField(queryset=Fournisseurs.objects.all(),
                   widget=forms.Select(attrs={'class': 'form-control custom-text-input',
                                              'id':'id_fournisseur',
                                              'name':'formunisseur'}),
                   )
    class Meta:
        model = CommandeSav
        fields = ( 'savrequest', 'fournisseur', 'nombre_jour', 'statut','commentaire')

        widgets = {
            'nombre_jour' : forms.NumberInput(attrs={'class': 'form-control custom-number-input',
                                                       'id':'id_nombre_jour',
                                                       'name':'nombre_jour'}),
            'savrequest' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_savrequest'}),
            'statut' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 
                                                       'id':'id_statut'}),        #                                          
            'commentaire' : forms.Textarea(attrs={'class': 'form-control custom-textarea',
                                                       'id':'id_commentaire',
                                                       'name':'commentaire'}),
            
        }
