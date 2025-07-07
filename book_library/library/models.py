import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

#--------------------------------------------------
# funciones de ayuda
#--------------------------------------------------
def validate_min_length(value):
    if len(value.strip()) < 3:
        raise ValidationError('Este campo debe tener al menos 3 caracteres.')

def validate_publish_year(value):
    current_year = datetime.date.today().year
    if value < 1700 or value > current_year:
        raise ValidationError(f'El año de publicación debe estar entre 1900 y {current_year}.')

#--------------------------------------------------
# modelos
#--------------------------------------------------   
class Category(models.Model):

    category_name = models.CharField(max_length=50,
                                    validators=[validate_min_length],
                                    unique=True,
                                    error_messages={
                                        'unique': 'Ya existe una categoria con ese nombre.',
                                    })
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Author(models.Model):
    name = models.CharField(max_length=50,
                            validators=[validate_min_length],
                            unique=True,
                            error_messages={
                                'unique': 'Ya existe un autor con ese nombre.',
                            })

    def __str__(self):
        return self.name

class Book(models.Model):

    STATUS_CHOICES = [
        ('A', 'Disponible'),
        ('B', 'Prestado'),
        ('U', 'No disponible'),
    ]
 
    library_code = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{2}-\d{3}$',
                message='El código debe tener el formato 99-999',
                )    
            ],
            unique=True,
            error_messages={
                'unique': 'Ya existe un libro con ese código.',
                }
    )
    title = models.CharField(max_length=50,
                             validators=[validate_min_length])
    isbn = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^\d{3}-\d{2}-\d{5}-\d{2}-\d{1}$',
                message='El ISBN debe tener el formato 999-99-99999-99-9',
            )
        ]
    )
    short_description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    editor = models.CharField(max_length=70,
                             validators=[validate_min_length])
    publish_year = models.IntegerField(
        validators=[validate_publish_year]
    )
    image = models.CharField(max_length=200, blank=True, null=True)    
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    aquisition_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
