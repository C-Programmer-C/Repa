from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api_urls')),  # API endpoints
    path('', include('core.urls')),  # Existing Django URLs
    path('login/',
         auth_views.LoginView.as_view(template_name='core/login.html'),
         name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

# Add this to serve the Vue app in production
urlpatterns += [
    path('app/', TemplateView.as_view(template_name='index.html'), name='vue_app'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)