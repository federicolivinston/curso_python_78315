from django import forms
from .models import Category, Author, Book

#--------------------------------------------------
# formularios de filtrado
#--------------------------------------------------

class BookFilterForm(forms.Form):
    isbn = forms.CharField(label="ISBN:", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '999‑99‑99999‑99‑9'
    }))
    library_code = forms.CharField(label="Código de biblioteca:", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '99‑999'
    }))
    title_contains = forms.CharField(label="Título: (contiene)", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Buscar por título...'
    }))

class CategoryFilterForm(forms.Form):
    name_contains = forms.CharField(
        label="Nombre: (contiene)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    is_active = forms.ChoiceField(
        label="Estado:",
        required=False,
        choices=[('', 'Todos'), ('1', 'Activa'), ('0', 'Inactiva')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AuthorFilterForm(forms.Form):
    name_contains = forms.CharField(
        label="Nombre: (contiene)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre de autor...'
        })
    )

#--------------------------------------------------
# formulario create / update de libros
#--------------------------------------------------

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'library_code', 'title', 'isbn', 'short_description',
            'category', 'author', 'editor', 'publish_year', 'image', 
            'status', 'user_booking', 'aquisition_date'
        ]

        labels = {
            'library_code': 'Código de biblioteca',
            'title': 'Título del libro',
            'isbn': 'ISBN',
            'short_description': 'Descripción breve',
            'category': 'Categoría',
            'author': 'Autor',
            'editor': 'Editorial',
            'publish_year': 'Año de publicación',
            'image': 'Imagen (opcional)',
            'status': 'Estado',
            'user_booking': 'Reservado por',
            'aquisition_date': 'Fecha Ingreso',
        }

        widgets = {
            'library_code': forms.TextInput(attrs={
                'placeholder': '99-999',
                'class': 'form-control'
            }),
            'isbn': forms.TextInput(attrs={
                'placeholder': '999-99-99999-99-9',
                'class': 'form-control'
            }),
            'short_description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Descripción breve del libro'
            }),
            'aquisition_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
        labels = {
            'name': 'Nombre del autor',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'active']
        labels = {
            'category_name': 'Nombre de la categoría',
            'active': '¿Está activa?',
        }
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
