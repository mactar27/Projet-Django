from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.template.defaulttags import register
from django.db import transaction, IntegrityError
from .models import Etudiant, Document, Filiere, Bulletin, ResponsableFiliere
from .forms import EtudiantForm, FormulaireInscription, DocumentForm, FiliereForm, BulletinForm

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Décorateur pour vérifier si l'utilisateur appartient au groupe 'etudiant'
def etudiant_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='etudiant').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Accès réservé aux étudiants.")
    return _wrapped_view

# Décorateur pour vérifier si l'utilisateur appartient au groupe 'admin'
def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Accès réservé aux administrateurs.")
    return _wrapped_view

# Décorateur pour vérifier si l'utilisateur appartient au groupe 'responsable_filiere'
def responsable_filiere_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='responsable_filiere').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Accès réservé aux responsables de filière.")
    return _wrapped_view

def inscription(request):
    form = FormulaireInscription()
    if request.method == 'POST':
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            with transaction.atomic():
                try:
                    user = form.save()
                    # Créer un profil Etudiant vide pour le nouvel utilisateur
                    Etudiant.objects.create(utilisateur=user)
                    # Ajouter l'utilisateur au groupe 'etudiant'
                    etudiant_group, created = Group.objects.get_or_create(name='etudiant')
                    user.groups.add(etudiant_group)
                    messages.success(request, 'Le compte a été créé pour ' + user.username)
                    return redirect('login')
                except Exception as e:
                    if isinstance(e, IntegrityError):
                        messages.error(request, "Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
                    else:
                        messages.error(request, 'Erreur lors de la création du compte. Veuillez réessayer.')
    return render(request, 'inscription.html', {'formulaire': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')  
        password = request.POST.get('password')
        utilisateur = authenticate(request, username=username, password=password)
        if utilisateur is not None:
            auth_login(request, utilisateur) 
            return redirect('home')
        else:
            messages.info(request, 'Login ou mot de passe incorrect')
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@etudiant_required
def apprenants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'etudiants.html', {'etudiants': etudiants})


@etudiant_required
def profil_utilisateur(request):
    etudiant=request.user.etudiant
    formulaire=EtudiantForm(instance=etudiant)
    if request.method=='POST':
        formulaire=EtudiantForm(request.POST,request.FILES,instance=etudiant)
        if formulaire.is_valid():
            formulaire.save()
            # return redirect('profil_utilisateur')
    context={'formulaire':formulaire}
    return render(request, 'profil_utilisateur.html',context)


@etudiant_required
def details(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)
    return render(request, 'details.html', {'etudiant': etudiant})

def home(request):
    etudiants_count = Etudiant.objects.count()
    cours_count = "50+"  # Valeur par défaut, peut être dynamique si vous avez un modèle Cours
    satisfaction = "98%"  # Valeur par défaut

    context = {
        'etudiants_count': etudiants_count,
        'cours_count': cours_count,
        'satisfaction': satisfaction,
    }
    return render(request, 'home.html', context)

def main(request):
    return render(request, 'main.html')

@login_required
def cours_view(request):
    """Vue pour les cours et ressources pédagogiques"""
    context = {
        'titre_page': 'Cours et Ressources',
        'description': 'Explorez les ressources pédagogiques et cours disponibles'
    }
    return render(request, 'cours.html', context)

def profile(request):
    return render(request, 'profile.html')

@admin_required
def admin_view_etudiants(request):
    """Vue admin pour voir tous les étudiants"""
    etudiants = Etudiant.objects.all()
    filieres = Filiere.objects.all()
    return render(request, 'admin_etudiants.html', {'etudiants': etudiants, 'filieres': filieres})

@etudiant_required
def etudiant_view_profil(request):
    """Vue étudiant pour voir son propre profil"""
    etudiant = request.user.etudiant
    return render(request, 'etudiant_profil.html', {'etudiant': etudiant})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.utilisateur = request.user
            document.save()
            messages.success(request, 'Document téléchargé avec succès!')
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

@login_required
def liste_documents(request):
    documents = Document.objects.filter(utilisateur=request.user).order_by('-date_upload')
    return render(request, 'liste_documents.html', {'documents': documents})

@admin_required
def gerer_filieres(request):
    filieres = Filiere.objects.all().order_by('nom')
    form = FiliereForm()

    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Filière créée avec succès!')
            return redirect('gerer_filieres')

    context = {
        'filieres': filieres,
        'form': form,
    }
    return render(request, 'gerer_filieres.html', context)

@admin_required
def assigner_etudiant_filiere(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    filieres = Filiere.objects.all()

    if request.method == 'POST':
        filiere_id = request.POST.get('filiere')
        if filiere_id:
            filiere = get_object_or_404(Filiere, id=filiere_id)
            etudiant.filiere = filiere
            etudiant.save()
            messages.success(request, f'{etudiant.prenom} {etudiant.nom} a été assigné à la filière {filiere.nom}')
        else:
            etudiant.filiere = None
            etudiant.save()
            messages.success(request, f'{etudiant.prenom} {etudiant.nom} a été retiré de sa filière')
        return redirect('admin_etudiants')

    context = {
        'etudiant': etudiant,
        'filieres': filieres,
    }
    return render(request, 'assigner_filiere.html', context)

@admin_required
def etudiants_par_filiere(request, filiere_id=None):
    if filiere_id:
        filiere = get_object_or_404(Filiere, id=filiere_id)
        etudiants = Etudiant.objects.filter(filiere=filiere)
        titre = f"Étudiants en {filiere.nom}"
    else:
        etudiants = Etudiant.objects.filter(filiere__isnull=True)
        titre = "Étudiants sans filière"

    filieres = Filiere.objects.all()

    context = {
        'etudiants': etudiants,
        'filieres': filieres,
        'titre': titre,
        'filiere_courante': filiere if filiere_id else None,
    }
    return render(request, 'etudiants_par_filiere.html', context)

@admin_required
def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)

    if request.method == 'POST':
        # Supprimer l'utilisateur associé
        user = etudiant.utilisateur
        etudiant.delete()
        user.delete()
        messages.success(request, f'L\'étudiant {etudiant.prenom} {etudiant.nom} a été supprimé avec succès.')
        return redirect('admin_etudiants')

    context = {
        'etudiant': etudiant,
    }
    return render(request, 'supprimer_etudiant.html', context)

@admin_required
def gerer_bulletins(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    bulletins = Bulletin.objects.filter(etudiant=etudiant).order_by('-date_upload')
    form = BulletinForm()

    if request.method == 'POST':
        form = BulletinForm(request.POST, request.FILES)
        if form.is_valid():
            bulletin = form.save(commit=False)
            bulletin.etudiant = etudiant
            bulletin.save()
            messages.success(request, 'Bulletin/certificat ajouté avec succès!')
            return redirect('gerer_bulletins', etudiant_id=etudiant_id)

    context = {
        'etudiant': etudiant,
        'bulletins': bulletins,
        'form': form,
    }
    return render(request, 'gerer_bulletins.html', context)

@admin_required
def supprimer_bulletin(request, bulletin_id):
    bulletin = get_object_or_404(Bulletin, id=bulletin_id)
    etudiant_id = bulletin.etudiant.id
    bulletin.delete()
    messages.success(request, 'Bulletin/certificat supprimé avec succès!')
    return redirect('gerer_bulletins', etudiant_id=etudiant_id)

@admin_required
def admin_dashboard(request):
    etudiants_count = Etudiant.objects.count()
    filieres_count = Filiere.objects.count()
    context = {
        'etudiants_count': etudiants_count,
        'filieres_count': filieres_count,
    }
    return render(request, 'pages/admin_dashboard.html', context)

@responsable_filiere_required
def responsable_filiere_dashboard(request):
    responsable = get_object_or_404(ResponsableFiliere, utilisateur=request.user)
    filiere = responsable.filiere
    etudiants = Etudiant.objects.filter(filiere=filiere)
    context = {
        'filiere': filiere,
        'etudiants': etudiants,
    }
    return render(request, 'pages/responsable_filiere_dashboard.html', context)

@etudiant_required
def etudiant_dashboard(request):
    etudiant = request.user.etudiant
    context = {
        'etudiant': etudiant,
    }
    return render(request, 'pages/etudiant_dashboard.html', context)