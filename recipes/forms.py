from django import forms

from . import models


class UploadXMLFileForm(forms.Form):
    file = forms.FileField()


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['status', 'recipe']


class BrewSessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['pre_boil_vol', 'post_boil_vol',
                  'pre_boil_grav', 'post_boil_grav']
