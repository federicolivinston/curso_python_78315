from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

# importacion de vistas por modelo
from .views import user_login, register_view, ProfileView, avatar_update, update_profile, update_password   

urlpatterns = [
    path('users/login/', user_login, name='login'),
    path('users/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('users/registro/', register_view, name='registro'),
    path('users/perfil/', ProfileView.as_view(), name='perfil usuario'),
    path('users/avatar/editar/', avatar_update, name='actualizar avatar'),
    path('users/perfil/editar/', update_profile, name='actualizar perfil'),
    path('users/perfil/cambiarPassword/', update_password, name='actualizar password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)