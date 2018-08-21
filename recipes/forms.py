from django import forms

from . import models


class UploadXMLFileForm(forms.Form):
    file = forms.FileField()


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = '__all__'
