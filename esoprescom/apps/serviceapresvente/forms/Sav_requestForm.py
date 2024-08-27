from django import forms
from apps.serviceapresvente.models.Sav_request import Sav_request
from apps.serviceapresvente.models.Personnels import Personnels
from apps.serviceapresvente.models.Client_sav import Client_sav
from apps.serviceapresvente.models.Partenaires import Partenaires

class Sav_requestForm(forms.ModelForm):
    SAV_TYPE= [("DEVEA","DEVEA"),
              ("Non DEVEA","Non DEVEA")]
    """
    type_sav = forms.ChoiceField(choices=SAV_TYPE,
                                 widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
                                                             'id': 'id_type_SAV'}),
                                 initial='Non DEVEA'
    )       

    STATUS_GARANTIE = [("Sous garantie","Sous garantie"),
                       ("Hors garantie","Hors garantie")]
    garantie = forms.ChoiceField(choices=STATUS_GARANTIE,
                                   widget=forms.RadioSelect(attrs={'class': 'form-control custom-text-input',
                                                              'id': 'id_garantie'}),
                                   initial="Hors garantie"
    )
    """       
    client_sav = forms.ModelChoiceField(queryset=Client_sav.objects.filter(is_active=True, is_deleted=False),
                   widget=forms.Select(attrs={'class': 'form-control custom-text-input',}),
                   )
     
    resp_sav = forms.ModelChoiceField(queryset=Personnels.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control custom-text-input'}),
    )
    marque = forms.ModelChoiceField(queryset=Partenaires.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control custom-text-input'}),
    )
 
    class Meta:
        model = Sav_request
        fields = ('type_sav',  'numero_fiche_technique', 'marque', 'client_sav', 'resp_sav', 'numero_serie', 'reference', 'designation', 'garantie', 'description_piece', 'reference_piece', 'pop', 'statut', 'observation',  'rapport_technique', 'facture_fournisseur', 'facture_proforma', 'bon_pour_accord','recouvrement_hp')
        # exclude = ['numero_dossier']
        widgets = {
            'type_sav': forms.RadioSelect(attrs={'class': 'form-check form-check-inline', 'id': 'id_type_SAV'}),
            'numero_fiche_technique' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            # 'numero_dossier' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'numero_serie' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'reference' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'designation' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'garantie' : forms.RadioSelect(attrs={'class': 'form-check form-check-inline','id': 'id_garantie'}),
            'description_piece' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'reference_piece' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'pop' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'statut' : forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'observation' : forms.Textarea(attrs={'class': 'form-control custom-textarea'}),
            'rapport_technique' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
                                                                  'id': 'id_rapport_technique'}),
            'facture_fournisseur' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
                                                                    'id': 'id_facture_fournisseur',
                                                                    }),
            'facture_proforma' : forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input',
                                                                 'id': 'id_facture_proforma',
                                                                 }),
            'bon_pour_accord' : forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                           'id':'id_bon_pour_accord'}),
            'recouvrement_hp' : forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                           'id':'id_recouvrement_hp'
                                                           }),
                                                           
            #'updated_at' : forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
           
        }
