from django.contrib import admin
from .models import Etudiant


class EtudiantAdmin(admin.ModelAdmin):
  list_display = ("prenom", "nom","telephone","adresse" ,"date",)

admin.site.register(Etudiant,EtudiantAdmin)

