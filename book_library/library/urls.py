from django.urls import path
# importacion de vistas por modelo

from .views import home, about_us
from .views import author_list, AuthorCreateView, AuthorUpdateView, AuthorDeleteView 
from .views import category_list, CategoryCreateView, CategoryDeleteView,CategoryUpdateView
from .views import book_list, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, book_reserve, book_return    

urlpatterns = [
    path('', home, name='inicio'),
    path('conocenos/', about_us, name='conocenos'),
    path('libros/', book_list, name='listado libros'),
    path('libros/<int:pk>/detalle/', BookDetailView.as_view(), name='detalle libro'),
    path('libros/nuevo/', BookCreateView.as_view(), name='nuevo libro'),
    path('libros/<int:pk>/editar/', BookUpdateView.as_view(), name='editar libro'),
    path('libros/eliminar/<int:pk>/', BookDeleteView.as_view(), name='eliminar libro'),
    path('libros/<int:pk>/reservar/', book_reserve, name='reservar libro'),
    path('libros/<int:pk>/devolver/', book_return, name='devolver libro'),
    path('categorias/', category_list, name='listado categorias'),
    path('categorias/nueva/', CategoryCreateView.as_view(), name='nueva categoria'),
    path('categorias/<int:pk>/editar/', CategoryUpdateView.as_view(), name='editar categoria'),
    path('categorias/eliminar/<int:pk>/', CategoryDeleteView.as_view(), name='eliminar categoria'),
    path('autores/', author_list, name='listado autores'),
    path('autores/nuevo/', AuthorCreateView.as_view(), name='nuevo autor'),
    path('autores/<int:pk>/editar/', AuthorUpdateView.as_view(), name='editar autor'),
    path('autores/eliminar/<int:pk>/', AuthorDeleteView.as_view(), name='eliminar autor')
]