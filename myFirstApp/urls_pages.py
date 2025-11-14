from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('responsable-filiere/', views.responsable_filiere_dashboard, name='responsable_filiere_dashboard'),
    path('etudiant/', views.etudiant_dashboard, name='etudiant_dashboard'),
]