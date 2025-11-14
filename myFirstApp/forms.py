# your_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Etudiant, Document, Filiere, Bulletin



class FormulaireInscription(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class EtudiantForm(ModelForm):
        class Meta:
            model = Etudiant
            fields = "__all__"
            exclude = ['utilisateur']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['titre', 'fichier']

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom', 'description']

class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['titre', 'type_document', 'fichier', 'annee_scolaire', 'semestre']