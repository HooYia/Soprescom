from django import forms
from apps.serviceapresvente.models.Sav_request import Sav_request
from apps.serviceapresvente.models.Personnels import Personnels
from apps.serviceapresvente.models.Client_sav import Client_sav
from apps.serviceapresvente.models.Partenaires import Partenaires

class DeveaForm(forms.ModelForm):
    ETAT = [("facturation HP, a completer","facturation HP, a completer"),
            ("Dossier HP  complet","Dossier HP  complet"),
            ("payé","payé"),
            ("non payé","non payé")]
    statut = forms.ChoiceField(choices=ETAT,
                                 widget=forms.Select(attrs={'class': 'form-control custom-text-input'}),
    )        
    
    class Meta:
        model = Devea
        fields = ('livraisonclient','statut','flag')
