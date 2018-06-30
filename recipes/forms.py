from django import forms

from . import models


class UploadXMLFileForm(forms.Form):
    file = forms.FileField()
