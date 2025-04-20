from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import json

from .models import HelpRequest, Application, User
from .forms import VolunteerSignupForm, VeteranSignupForm

# Utility functions
def serialize_request(request_obj):
    """Serialize a HelpRequest object to a dictionary for JSON response"""
    return {
        'id': request_obj.id,
        'help_type': request_obj.help_type,
        'type_display': request_obj.get_help_type_display(),
        'description': request_obj.description,
        'location': request_obj.location,
        'status': request_obj.status,
        'status_display': request_obj.get_status_display(),
        'created_at': request_obj.created_at.isoformat(),
        'veteran_id': request_obj.veteran.id if request_obj.veteran else None,
        'veteran_name': request_obj.veteran.username if request_obj.veteran else None,
    }

def serialize_user(user):
    """Serialize a User object to a dictionary for JSON response"""
    return {
        'id': user.id,
        'username': user.username,
        'email': getattr(user, 'email', ''),
        'role': user.role,
        'city': user.city,
        'phone': user.phone,
        'is_veteran': user.is_veteran(),
        'is_volunteer': user.is_volunteer(),
    }

# Authentication API endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """API endpoint for user login"""
    data = json.loads(request.body)
    username = data.get('username', '')
    password = data.get('password', '')
    user_type = data.get('user_type', '')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Check user type if specified
        if user_type == 'veteran' and not user.is_veteran():
            return Response({'error': 'Неверный тип пользователя'}, status=status.HTTP_403_FORBIDDEN)
        elif user_type == 'volunteer' and not user.is_volunteer():
            return Response({'error': 'Неверный тип пользователя'}, status=status.HTTP_403_FORBIDDEN)
            
        login(request, user)
        return Response({
            'user': serialize_user(user),
            'csrfToken': get_token(request)
        })
    else:
        return Response({'error': 'Неверное имя пользователя или пароль'}, 
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """API endpoint for user registration"""
    data = json.loads(request.body)
    user_type = data.get('user_type', '')
    
    if user_type == 'volunteer':
        form = VolunteerSignupForm(data)
    elif user_type == 'veteran':
        form = VeteranSignupForm(data)
    else:
        return Response({'error': 'Неверный тип пользователя'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if form.is_valid():
        user = form.save()
        login(request, user)
        return Response({
            'user': serialize_user(user),
            'csrfToken': get_token(request)
        })
    else:
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_api(request):
    """API endpoint to get current logged-in user info"""
    return Response({'user': serialize_user(request.user)})

# Help request API endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_list_api(request):
    """API endpoint to get list of help requests"""
    # Filter by status if provided
    status_filter = request.GET.get('status', None)
    help_type = request.GET.get('help_type', None)
    
    qs = HelpRequest.objects.all()
    
    if status_filter:
        qs = qs.filter(status=status_filter)
    
    if help_type:
        qs = qs.filter(help_type=help_type)
    
    # Filter by user role
    if request.user.is_veteran():
        qs = qs.filter(veteran=request.user)
    
    # Serialize the queryset
    requests_data = [serialize_request(req) for req in qs]
    
    return Response({'requests': requests_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_detail_api(request, pk):
    """API endpoint to get details of a specific help request"""
    help_request = get_object_or_404(HelpRequest, pk=pk)
    
    # Get applications if user is the veteran who created this request
    applications = []
    if request.user.is_veteran() and help_request.veteran == request.user:
        applications = [
            {
                'id': app.id,
                'volunteer_id': app.volunteer.id,
                'volunteer_name': app.volunteer.username,
                'contact_info': app.contact_info,
                'created_at': app.created_at.isoformat(),
            }
            for app in help_request.applications.all()
        ]
    
    # Check if current user has applied
    has_applied = False
    if request.user.is_volunteer():
        has_applied = help_request.applications.filter(volunteer=request.user).exists()
    
    response_data = {
        'request': serialize_request(help_request),
        'applications': applications,
        'has_applied': has_applied,
    }
    
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request_api(request):
    """API endpoint to create a new help request"""
    if not request.user.is_veteran():
        return Response({'error': 'Только ветераны могут создавать заявки'}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    data = json.loads(request.body)
    help_request = HelpRequest(
        veteran=request.user,
        help_type=data.get('help_type', ''),
        description=data.get('description', ''),
        location=data.get('location', ''),
        status='open'
    )
    
    try:
        help_request.full_clean()
        help_request.save()
        return Response({'request': serialize_request(help_request)})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_request_api(request, pk):
    """API endpoint for a volunteer to respond to a help request"""
    if not request.user.is_volunteer():
        return Response({'error': 'Только волонтеры могут откликаться на заявки'}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    help_request = get_object_or_404(HelpRequest, pk=pk)
    
    # Check if already applied
    if help_request.applications.filter(volunteer=request.user).exists():
        return Response({'error': 'Вы уже откликнулись на эту заявку'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    data = json.loads(request.body)
    application = Application(
        help_request=help_request,
        volunteer=request.user,
        contact_info=data.get('contact_info', '')
    )
    
    try:
        application.full_clean()
        application.save()
        return Response({'success': True})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_request_api(request, pk):
    """API endpoint to mark a help request as completed"""
    help_request = get_object_or_404(HelpRequest, pk=pk)
    
    # Only the veteran who created the request can mark it as completed
    if not request.user.is_veteran() or help_request.veteran != request.user:
        return Response({'error': 'У вас нет прав для выполнения этого действия'}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    help_request.status = 'done'
    help_request.save()
    
    return Response({'success': True})

# Existing Unity API endpoints (imported from views.py)
from .views import api_requests, api_respond 

# Simple test API endpoint
@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    """A simple API endpoint for testing the Vue.js integration"""
    return Response({
        'message': 'API is working properly',
        'status': 'success'
    }) 