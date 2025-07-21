# Imports generales
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from typing import cast
from .forms import RegisterForm
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Avatar  
from .forms import AvatarForm, UserUpdateForm, CustomPasswordChangeForm

#--------------------------------------------------
# vistas de acceso al portal (login y registro)
#--------------------------------------------------

def user_login(request):
    if request.user.is_authenticated:
         return redirect('inicio')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('inicio')
        else:
            form = AuthenticationForm()
    
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    return render(request, 'library_user/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, 'library_user/register.html', {'form': form})

#--------------------------------------------------
# Vista para mostrar el perfil con el avatar
#--------------------------------------------------

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'library_user/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avatar = Avatar.objects.filter(user=self.request.user).first()
        context['avatar'] = avatar
        context['avatar_form'] = AvatarForm(instance=avatar)
        context['profile_form'] = UserUpdateForm(instance=self.request.user)
        context['password_form'] = CustomPasswordChangeForm(user=self.request.user)
        return context

#--------------------------------------------------
# vistas para administrar el avatar, 
# el perfil y la password
#--------------------------------------------------

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil usuario')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'partials/profile_update_form.html', {'form': form})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def avatar_update(request):
    avatar, created = Avatar.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avatar actualizado correctamente.')
        else:
            messages.error(request, 'Error al actualizar el avatar.')
    return redirect('perfil usuario')
    
@login_required
def update_password(request):
    user = request.user
    abrir_modal = request.method == 'POST'

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, "Contraseña cambiada correctamente.")
            return redirect('perfil usuario')
        
    else:
        form = CustomPasswordChangeForm(user=user)

    avatar = Avatar.objects.filter(user=user).first()

    return render(request, 'library_user/profile.html', {
        'avatar': avatar,
        'avatar_form': AvatarForm(instance=avatar),
        'profile_form': UserUpdateForm(instance=user),
        'password_form': form,
        'abrir_modal': abrir_modal
    })


