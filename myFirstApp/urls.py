from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('myFirstApp/', views.apprenants, name='etudiants'),
    path('myFirstApp/details/<int:id>', views.details,name='details'),
    # path('', views.main, name='main'),
    path('cours/', views.cours_view, name='cours'),
    path('', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profil_utilisateur/', views.profil_utilisateur ,name='profil_utilisateur'),
    path('admin/etudiants/', views.admin_view_etudiants, name='admin_etudiants'),
    path('etudiant/profil/', views.etudiant_view_profil, name='etudiant_profil'),
    #les url pour le reset du mot de passe
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),

    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),

    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name='password_reset_complete'),

    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.liste_documents, name='liste_documents'),

    # URLs admin pour les filières
    path('admin/filieres/', views.gerer_filieres, name='gerer_filieres'),
    path('admin/etudiant/<int:etudiant_id>/assigner-filiere/', views.assigner_etudiant_filiere, name='assigner_filiere'),
    path('admin/filieres/<int:filiere_id>/etudiants/', views.etudiants_par_filiere, name='etudiants_par_filiere'),
    path('admin/etudiants-sans-filiere/', views.etudiants_par_filiere, {'filiere_id': None}, name='etudiants_sans_filiere'),

    # URLs admin pour suppression et bulletins
    path('admin/etudiant/<int:etudiant_id>/supprimer/', views.supprimer_etudiant, name='supprimer_etudiant'),
    path('admin/etudiant/<int:etudiant_id>/bulletins/', views.gerer_bulletins, name='gerer_bulletins'),
    path('admin/bulletin/<int:bulletin_id>/supprimer/', views.supprimer_bulletin, name='supprimer_bulletin'),

]