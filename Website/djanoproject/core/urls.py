from django.urls import path
from . import views

urlpatterns = [
    path('signup/volunteer/', views.signup_volunteer,  name='signup_volunteer'),
    path('signup/veteran/',   views.signup_veteran,    name='signup_veteran'),
    path('requests/',         views.request_list,      name='request_list'),
    path('requests/create/',  views.create_request,    name='create_request'),
    path('requests/<int:pk>/',        views.request_detail, name='request_detail'),
    path('requests/<int:pk>/respond/',views.respond_request,name='respond_request'),
    path('dashboard/',        views.dashboard,         name='dashboard'),
    path('dashboard/<int:pk>/revoke/',views.revoke_request,name='revoke_request'),
    path('dashboard/<int:pk>/status/',views.update_status, name='update_status'),
    
    # API для Unity-приложения
    path('api/requests/',     views.api_requests,      name='api_requests'),
    path('api/respond/',      views.api_respond,       name='api_respond'),
    path('unity-map/',        views.unity_map,         name='unity_map'),

    # Маршрут для Vue.js приложения с использованием CDN
    path('vue/', views.vue_app_cdn, name='vue_app_cdn'),
]