from django.contrib import admin
from .models import Book, Category, Author

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'publish_year', 'status')
    search_fields = ('title', 'isbn', 'author__name')
    list_filter = ('status', 'category', 'publish_year')
    ordering = ('-aquisition_date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'active')
    search_fields = ('category_name',)
    list_filter = ('active',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
