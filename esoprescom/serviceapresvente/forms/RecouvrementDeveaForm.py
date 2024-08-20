from django import forms
from serviceapresvente.models.Recouvrement import Recouvrement



class RecouvrementDeveaForm(forms.ModelForm):
    ETAT = [("facturation HP, à completer","facturation HP, à completer"),
            ("Dossier HP complet","Dossier HP complet"),
            ("Dossier HP payé","Dossier HP payé")]
    #statutDevea = forms.ChoiceField(choices=ETAT,
    #                             widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
    #                                                        'id':'id_recouvrementstatut'}),
    #                             initial='facturation HP, à completer'
    #)   
    TRANSIT = [("TANSIT1","TANSIT1"),
               ("TANSIT2","TANSIT2")]
        
    transitaire = forms.ChoiceField(choices=TRANSIT,
                                 widget=forms.Select(attrs={'class': 'form-control custom-text-input'}),
    )      
    class Meta:
        model = Recouvrement
        fields = ('livraisonclient','is_devea_request','deveaOrder','statutDevea','numero_awd','montant_prestation','remise_documentaire','droit_douane','transport','facture_transitaire','autre_piece')

        widgets = {
            'statutDevea' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 
                                                       'id':'id_recouvrementstatut'}), 
            'livraisonclient' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                       'id':'id_livraisonclient'}),
            'is_devea_request' : forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                           'id':'id_is_devea_request',
                                                           'disabled':'disabled'}),
            'deveaOrder' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                  'id':'id_deveaOrder'
                                               }),
            'numero_awd' : forms.TextInput(attrs={'class': 'form-control custom-text-input',
                                                  'id':'id_numero_awd'
                                               }),
            'montant_prestation' : forms.NumberInput(attrs={'class': 'form-control custom-text-input',
                                                                     'id':'id_montant_prestation',
                                                                     'placeholder': 'Enter amount',
                                                  }),
            'remise_documentaire' : forms.NumberInput(attrs={'class': 'form-control custom-text-input',
                                                                     'placeholder': 'Montant remise documentaire',
                                                  }),
            'droit_douane' : forms.NumberInput(attrs={'class': 'form-control custom-text-input',
                                                                     'placeholder': 'Droit douane',
                                                  }),
            'transport' : forms.NumberInput(attrs={'class': 'form-control custom-text-input',
                                                                     'placeholder': 'Montant transport',
                                                  }),
            'facture_transitaire' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
                                                                  'id': 'id_facture_transitaire',
                                                                  'placeholder': 'Fichier facture transitaire',
                                                                  }),
           
            'autre_piece' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
            })
        }