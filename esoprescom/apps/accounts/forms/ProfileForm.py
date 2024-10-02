from django import forms
from apps.accounts.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'first_name', 'last_name','organisation','location','email', 'address', 'contact', 'profession']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'form-control-file'})    
