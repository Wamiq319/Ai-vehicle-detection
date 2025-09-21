from django.shortcuts import redirect
from django.urls import reverse


class AuthenticationRedirectMiddleware:
    """
    Middleware to redirect authenticated users away from login page to dashboard
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and trying to access login page
        if (request.user.is_authenticated and 
            request.path == '/accounts/login/' and 
            request.method == 'GET'):
            return redirect('dashboard')
        
        response = self.get_response(request)
        return response