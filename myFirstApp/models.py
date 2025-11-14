from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField

class Filiere(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Etudiant(models.Model):
  utilisateur = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  prenom = models.CharField(max_length=255, null=True, blank=True)
  nom = models.CharField(max_length=255, null=True, blank=True)
  telephone=models.IntegerField(null=True)
  adresse=models.CharField(null=True,max_length=255)
  date=models.DateField(null=True)
  imageProfil=models.ImageField(null=True, blank=True)
  filiere = models.ForeignKey(Filiere, null=True, blank=True, on_delete=models.SET_NULL)

  def __str__(self):
    return f"{self.prenom} {self.nom}"

class ResponsableFiliere(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    filiere = models.OneToOneField(Filiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"Responsable de {self.filiere.nom} - {self.utilisateur.username}"

class Bulletin(models.Model):
    TYPE_CHOICES = [
        ('bulletin', 'Bulletin de notes'),
        ('certificat', 'Certificat'),
        ('diplome', 'Diplôme'),
    ]

    titre = models.CharField(max_length=255)
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES, default='bulletin')
    fichier = models.FileField(upload_to='bulletins/')
    date_upload = models.DateTimeField(auto_now_add=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    annee_scolaire = models.CharField(max_length=20, blank=True)
    semestre = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.titre} - {self.etudiant.prenom} {self.etudiant.nom}"

class Document(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='documents/')
    date_upload = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre