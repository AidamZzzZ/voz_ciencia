from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import AdminLoginView, AdminDashboardView, CampanaCreateView, CampanaUpdateView, CampanaDeleteView, CampanaResultadosView

urlpatterns = [
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin-logout/', LogoutView.as_view(), name='admin_logout'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/campana/nueva/', CampanaCreateView.as_view(), name='campana_create'),
    path('admin-dashboard/campana/<int:pk>/editar/', CampanaUpdateView.as_view(), name='campana_update'),
    path('admin-dashboard/campana/<int:pk>/eliminar/', CampanaDeleteView.as_view(), name='campana_delete'),
    path('admin-dashboard/campana/<int:pk>/resultados/', CampanaResultadosView.as_view(), name='campana_resultados'),
]




