from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from petApp import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', include('petApp.urls'), name='petApp'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pet/add/', views.add_pet, name='add_pet'),
    path('pet/<str:pet_uuid>/', views.pet_profile, name='pet_profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),

    
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)