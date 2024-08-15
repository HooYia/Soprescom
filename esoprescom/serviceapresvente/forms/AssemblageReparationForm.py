from django import forms
from serviceapresvente.models.AssemblageReparation import AssemblageReparation

class AssemblageReparationForm(forms.ModelForm):
    ETAT=[("pending (DSI - Assemblage)","pending (DSI - Assemblage)"), 
         ("Terminé","Terminé")] 
     
    statut = forms.ChoiceField(choices=ETAT,
                                   widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
                                                              'id':'id_statut',
                                                              'name':'statut'}), 
                                   initial='pending (DSI - Assemblage)'
    )  
    class Meta:
        model = AssemblageReparation
        fields = ('suivicommandesav', 'statut','commentaire')

        widgets = {
            'suivicommandesav' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_suivicommandesav'}),
            'statut' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'commentaire' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
        }
