import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myFirstProject.settings')
django.setup()

from django.contrib.auth.models import User
from myFirstApp.models import Etudiant

user = User.objects.filter(username='wocky').first()
if user:
    print('User exists: True')
    etudiant = Etudiant.objects.filter(utilisateur=user).first()
    if etudiant:
        print('Associated Etudiant: True')
    else:
        print('Associated Etudiant: False')
else:
    print('User exists: False')