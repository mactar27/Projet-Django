#!/usr/bin/env python
"""
Script pour créer un utilisateur administrateur
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myFirstProject.settings')
django.setup()

from django.contrib.auth.models import User, Group

def create_admin_user():
    """Crée un utilisateur administrateur avec les permissions appropriées"""

    # Données de l'admin
    admin_data = {
        'username': 'admin',
        'email': 'admin@isep.edu',
        'password': 'admin123',
        'first_name': 'Administrateur',
        'last_name': 'ISEP'
    }

    try:
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=admin_data['username']).exists():
            print(f"L'utilisateur {admin_data['username']} existe déjà.")
            return

        # Créer l'utilisateur
        admin_user = User.objects.create_user(
            username=admin_data['username'],
            email=admin_data['email'],
            password=admin_data['password'],
            first_name=admin_data['first_name'],
            last_name=admin_data['last_name'],
            is_staff=True,
            is_superuser=True
        )

        # Créer et assigner le groupe admin
        admin_group, created = Group.objects.get_or_create(name='admin')
        admin_user.groups.add(admin_group)

        print("✅ Utilisateur administrateur créé avec succès!")
        print(f"   Nom d'utilisateur: {admin_data['username']}")
        print(f"   Email: {admin_data['email']}")
        print(f"   Mot de passe: {admin_data['password']}")
        print("   Groupe: admin")

    except Exception as e:
        print(f"❌ Erreur lors de la création de l'admin: {e}")
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'admin: {e}")

if __name__ == '__main__':
    create_admin_user()