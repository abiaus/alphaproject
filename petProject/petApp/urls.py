from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from petApp import views
from django.contrib.auth import views as auth_views



app_name = 'petApp'  # Asegúrate de que esta línea esté presente

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pet/add/', views.add_pet, name='add_pet'),
    path('pet/<str:pet_uuid>/', views.pet_profile, name='pet_profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('index.html', views.home, name='home'),
    path('pet/<str:pet_uuid>/edit_pet_visibility/', views.edit_pet_visibility, name='edit_pet_visibility'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_user_email/', views.edit_user_email, name='edit_user_email'),
    path('edit_user_details/', views.edit_user_details, name='edit_user_details'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),


    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
