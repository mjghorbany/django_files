from django import forms
from django.contrib.auth.models import User

from .models import Ontology


class OntologyForm(forms.ModelForm):

    class Meta:
        model = Ontology
        fields = ['domain', 'ontology_title', 'description', 'ontology_logo']



