from django.urls import path
from . import api_views

urlpatterns = [
    # API endpoints for Vue.js frontend
    path('requests/', api_views.request_list_api, name='api_request_list'),
    path('requests/<int:pk>/', api_views.request_detail_api, name='api_request_detail'),
    path('requests/<int:pk>/respond/', api_views.respond_request_api, name='api_respond_request'),
    path('requests/create/', api_views.create_request_api, name='api_create_request'),
    path('requests/<int:pk>/complete/', api_views.complete_request_api, name='api_complete_request'),
    
    # Authentication APIs
    path('login/', api_views.login_api, name='api_login'),
    path('register/', api_views.register_api, name='api_register'),
    path('user/', api_views.current_user_api, name='api_current_user'),
    
    # Existing Unity-related API endpoints
    path('unity-requests/', api_views.api_requests, name='api_unity_requests'),
    path('unity-respond/', api_views.api_respond, name='api_unity_respond'),
    
    # Test API endpoint
    path('test/', api_views.test_api, name='api_test'),
] 