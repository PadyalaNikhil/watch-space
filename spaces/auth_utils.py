import datetime
import jwt
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from .models import WatchUser


def generate_jwt_token(user: WatchUser) -> str:
    """
    Generates a secure JWT token for a user.
    """
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'display_name': user.display_name,
        'role': user.role,
        'avatar_initials': user.avatar_initials,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token: str):
    """
    Decodes and validates a JWT token.
    """
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_user_from_request(request):
    """
    Extracts and returns the authenticated WatchUser from request headers or query params.
    """
    auth_header = request.headers.get('Authorization', '')
    token = None
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    elif 'token' in request.GET:
        token = request.GET.get('token')
    elif request.COOKIES.get('token'):
        token = request.COOKIES.get('token')

    if not token:
        # Fallback to demo default user if specified in header or session
        demo_user_id = request.headers.get('X-Demo-User') or request.GET.get('demo_user')
        if demo_user_id:
            return WatchUser.objects.filter(id=demo_user_id).first()
        return None

    payload = decode_jwt_token(token)
    if not payload:
        return None

    return WatchUser.objects.filter(id=payload.get('user_id')).first()


def login_required_api(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_user_from_request(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized. Valid JWT token required.'}, status=401)
        request.watch_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = get_user_from_request(request)
            if not user:
                return JsonResponse({'error': 'Unauthorized. Valid JWT token required.'}, status=401)
            if user.role != required_role and user.role != 'admin':
                return JsonResponse({
                    'error': f'Forbidden: This action requires {required_role} role. Your role is {user.role}. Server-side RBAC enforced.'
                }, status=403)
            request.watch_user = user
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
