from django.shortcuts import redirect
from django.conf import settings
import re

# --------------------------------------------------------
# Este codigo genera que todas las paginas que 
# no esten exentas requieren que el usuario este logueado
# --------------------------------------------------------

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            re.compile(r'^$'),
            re.compile(r'^conocenos/?$'),               
            re.compile(r'^users/login/?$'),
            re.compile(r'^users/logout/?$'),
            re.compile(r'^users/registro/?$'),      
            re.compile(r'^admin/'),
            re.compile(r'^libros/?$'),  
            re.compile(r'^libros/\d+/detalle/?$'),
            re.compile(r'^media/'),  
        ]

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        if not request.user.is_authenticated:
            if not any(url.match(path) for url in self.exempt_urls):
                return redirect(f"{settings.LOGIN_URL}?next=/{path}")
        
        return self.get_response(request)
