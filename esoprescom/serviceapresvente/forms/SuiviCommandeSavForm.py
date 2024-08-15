from django import forms
from serviceapresvente.models.SuiviCommandeSav import SuiviCommandeSav

class SuiviCommandeSavForm(forms.ModelForm):
    ETAT=[("pending (logistique)","pending (logistique)"), 
    
    ("Sous Douane Malienne","Sous Douane Malienne"),
    ("Reçu","Reçu")]    
    
    statut = forms.ChoiceField(choices=ETAT,
                                   widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
                                                              'id':'id_statut',
                                                              'name':'statut'}), 
                                   initial='pending (logistique)'
    )  
    class Meta:
        model = SuiviCommandeSav
        fields = ('commandesav', 'statut', 'nombre_jour',  'commentaire')

        widgets = {
            'commandesav' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_commandesav'}),
            'nombre_jour' : forms.NumberInput(attrs={'class': 'form-control custom-number-input'}),
            'commentaire' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
        }
