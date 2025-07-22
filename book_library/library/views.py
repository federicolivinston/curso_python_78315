# Imports generales
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from typing import cast

# Import de modelos
from .models import Book, Category, Author, Parameter 

# Import de forms
from .forms import AuthorForm, BookFilterForm, BookForm, CategoryForm
from .forms import CategoryFilterForm
from .forms import AuthorFilterForm

#--------------------------------------------------
# vistas estaticas
#--------------------------------------------------
def home(request):
    return render(request, 'library/inicio.html')

def about_us(request):
    return render(request, 'library/about_us.html')

#--------------------------------------------------
# vistas de aministracion de libros (crud)
#--------------------------------------------------
def book_list(request):
    form = BookFilterForm(request.GET or None)
    libros = Book.objects.select_related('author', 'category').all()

    if form.is_valid():
        isbn = form.cleaned_data.get('isbn')
        library_code = form.cleaned_data.get('library_code')
        title = form.cleaned_data.get('title_contains')

        if isbn:
            libros = libros.filter(isbn__icontains=isbn)
        if library_code:
            libros = libros.filter(library_code__icontains=library_code)
        if title:
            libros = libros.filter(title__icontains=title)

    is_admin = request.user.groups.filter(name='admin').exists()

    context = {
        'form': form,
        'book_list': libros.order_by('title'),
        'is_admin': is_admin,
    }
    return render(request, 'library/book_list.html', context)

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/common_cu_form.html'
    success_url = reverse_lazy('listado libros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo libro:'
        context['cancel_url'] = reverse_lazy('listado libros')
        context['show_save_and_add'] = True
        return context
    
    def form_valid(self, form):
        try:
            self.object = form.save()
            if 'save_create_another' in self.request.POST:
                messages.success(self.request, '✅ Libro creado con éxito. Podés cargar otro.')
                return redirect('nuevo libro')
            messages.success(self.request, '✅ Libro guardado con éxito.')
            return redirect(self.get_success_url())
        except IntegrityError:
            form.add_error('name', '❌ Ya existe un libro con ese codigo de biblioteca.')
            return self.form_invalid(form)

    def form_invalid(self, form):
         messages.error(self.request, '❌ Ocurrió un error al guardar el libro. Revisá los campos.')
         return super().form_invalid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/common_cu_form.html'
    success_url = reverse_lazy('listado libros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar libro:'
        context['cancel_url'] = reverse_lazy('listado libros')
        context['show_save_and_add'] = False
        return context

    def form_valid(self, form):
        book = self.get_object()

        # Si se marcó "eliminar imagen"
        if self.request.POST.get('image-clear'):
            if book.image:
                book.image.delete(save=False)
            form.instance.image = None

        # Si no se subió una nueva, conservar la actual
        elif not self.request.FILES.get('image'):
            form.instance.image = book.image

        messages.success(self.request, "✅ Libro actualizado con éxito.")
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/common_confirm_delete.html'
    success_url = reverse_lazy('listado libros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = cast(Book, self.get_object())
        context['object_name'] = f'el libro "{obj.title}"'
        context['cancel_url'] = reverse_lazy('listado libros')
        return context

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "🗑️ Libro eliminado con éxito.")
            return response
        except ProtectedError:
            messages.error(request, "❌ No se puede eliminar el libro.")
            return redirect(self.success_url)

@login_required
def book_reserve(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # Cambiar estado a "Prestado"
        status_prestado = Parameter.objects.get(parameter_type='book_status', name='Prestado')
        book.status = status_prestado
        book.user_booking = request.user
        book.save()

    return redirect('detalle libro', pk=book.pk)

@login_required
def book_return(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST' and book.user_booking == request.user:
        status_disponible = Parameter.objects.get(parameter_type='book_status', name='Disponible')
        book.status = status_disponible
        book.user_booking = None
        book.save()

    return redirect('detalle libro', pk=book.pk)

#--------------------------------------------------
# vistas de administracion de categorias (crud)
#--------------------------------------------------
@login_required
def category_list(request):
    form = CategoryFilterForm(request.GET or None)
    categories = Category.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name_contains')
        active = form.cleaned_data.get('is_active')

        if name:
            categories = categories.filter(category_name__icontains=name)
        if active in ['0', '1']:
            categories = categories.filter(active=(active == '1'))
    is_admin = request.user.groups.filter(name='admin').exists()

    context = {
        'form': form,
        'categories': categories.order_by('category_name'),
        'is_admin': is_admin,
    }
    return render(request, 'library/category_list.html', context)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'library/common_cu_form.html'
    success_url = reverse_lazy('listado categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '➕ Nueva Categoría'
        context['cancel_url'] = self.success_url
        context['show_save_and_add'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'save_create_another' in self.request.POST:
            messages.success(self.request, '✅ Categoría creada con éxito. Podés cargar otra.')
            return redirect('nueva categoria')
        messages.success(self.request, '✅ Categoría guardada con éxito.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, '❌ Ocurrió un error al guardar la categoría. Revisá los campos.')
        return super().form_invalid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'library/common_cu_form.html'
    success_url = reverse_lazy('listado categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoria:'
        context['cancel_url'] = reverse_lazy('listado categorias')
        context['show_save_and_add'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Categoria actualizada con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Ocurrió un error al actualizar la categoria.")
        return super().form_invalid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'library/common_confirm_delete.html'
    success_url = reverse_lazy('listado categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = cast(Category, self.get_object())
        context['object_name'] = f'la categoria "{obj.category_name}"'
        context['cancel_url'] = reverse_lazy('listado categorias')
        return context

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "🗑️ Categoria eliminado con éxito.")
            return response
        except ProtectedError:
            messages.error(request, "❌ No se puede eliminar la categori porque tiene libros asociados.")
            return redirect(self.success_url)    
    
#--------------------------------------------------
# vistas de administracion de autores (crud)
#--------------------------------------------------
@login_required
def author_list(request):
    form = AuthorFilterForm(request.GET or None)
    authors = Author.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name_contains')
        if name:
            authors = authors.filter(name__icontains=name)
    is_admin = request.user.groups.filter(name='admin').exists()

    context = {
        'form': form,
        'authors': authors.order_by('name'),
        'is_admin': is_admin,
    }
    return render(request, 'library/author_list.html', context)

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/common_cu_form.html'
    success_url = reverse_lazy('listado autores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '➕ Nuevo Autor'
        context['cancel_url'] = self.success_url
        context['show_save_and_add'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'save_create_another' in self.request.POST:
            messages.success(self.request, '✅ Autor creado con éxito. Podés cargar otro.')
            return redirect('nuevo autor')  # Este name debe existir en tu urls.py
        messages.success(self.request, '✅ Autor guardado con éxito.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, '❌ Ocurrió un error al guardar el autor. Revisá los campos.')
        return super().form_invalid(form)

class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/common_cu_form.html'
    success_url = reverse_lazy('listado autores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Autor:'
        context['cancel_url'] = reverse_lazy('listado autores')
        context['show_save_and_add'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Autor actualizado con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Ocurrió un error al actualizar el autor.")
        return super().form_invalid(form)

class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = 'library/common_confirm_delete.html'
    success_url = reverse_lazy('listado autores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = cast(Author, self.get_object())
        context['object_name'] = f'el autor "{obj.name}"'
        context['cancel_url'] = reverse_lazy('listado autores')
        return context

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "🗑️ Autor eliminado con éxito.")
            return response
        except ProtectedError:
            messages.error(request, "❌ No se puede eliminar el autor porque tiene libros asociados.")
            return redirect(self.success_url)
