from django import forms
from .models import Book

#--------------------------------------------------
# formularios de filtrado
#--------------------------------------------------

class BookFilterForm(forms.Form):
    isbn = forms.CharField(label="ISBN", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '999‑99‑99999‑99‑9'
    }))
    library_code = forms.CharField(label="Código de biblioteca", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '99‑999'
    }))
    title_contains = forms.CharField(label="Título contiene", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Buscar por título...'
    }))

class CategoryFilterForm(forms.Form):
    name_contains = forms.CharField(
        label="Nombre contiene",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    is_active = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[('', 'Todos'), ('1', 'Activa'), ('0', 'Inactiva')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AuthorFilterForm(forms.Form):
    name_contains = forms.CharField(
        label="Nombre contiene",
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
            'category', 'author', 'editor', 'publish_year', 'image'
        ]

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
        }
