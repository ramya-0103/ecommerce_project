from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_views
from django.contrib.auth import views as django_auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User Authentication Paths
    path('login/', django_auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', django_auth_views.LoginView.as_view(template_name='registration/register.html'), name='register'),
    path('logout/', django_auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Include all app URLs (your custom views and API routes)
    path('', include('store.urls')), 
    
    # --- AUTHENTICATION ENDPOINT (DRF) ---
    path('api/token/', auth_views.obtain_auth_token, name='api_token_auth'),
]

# This is the critical part for serving images in a development environment.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
