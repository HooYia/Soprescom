from django import forms
from apps.serviceapresvente.models.AssemblageReparation import AssemblageReparation

class AssemblageReparationForm(forms.ModelForm):
    ETAT=[("pending (DSI - Assemblage)","pending (DSI - Assemblage)"), 
         ("Terminé","Terminé")] 
     
    
    class Meta:
        model = AssemblageReparation
        fields = ('suivicommandesav', 'statut','commentaire')

        widgets = {
            'suivicommandesav' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_suivicommandesav'}),
            'statut' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 
                                                       'id':'id_statut'}), 
            'commentaire' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
        }
