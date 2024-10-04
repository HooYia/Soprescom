from django import forms
from ..models.SortieLivraison import SortieLivraison

class SortieLivraisonForm(forms.ModelForm):
    class Meta:
        model = SortieLivraison
        fields = ['date', 'ol', 'ccial', 'fact', 'bdc', 'client', 'reference', 'designation', 'qte_dde', 'stock_initial', 'observation']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'ol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OL', 'required': 'required'}),
            'ccial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CCIAL', 'required': 'required'}),
            'fact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter FACT', 'required': 'required'}),
            'bdc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter BDC', 'required': 'required'}),
            'client': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),  # Select dropdown for client
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Reference', 'required': 'required'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation', 'required': 'required'}),
            'qte_dde': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity', 'required': 'required'}),
            'stock_initial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Stock Initial', 'required': 'required'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Observation', 'required': 'required'}),
        }
