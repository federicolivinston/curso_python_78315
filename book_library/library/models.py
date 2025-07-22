import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

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
# Función para generar la ruta de subida dinámica
#--------------------------------------------------

def book_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        return f'book_images/{instance.pk}.{ext}'
    return f'book_images/temp/{filename}'

#--------------------------------------------------
# storage personalizado para imágenes
#--------------------------------------------------

book_image_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url='/media/')

#--------------------------------------------------
# este modelo contiene los datos genericos inamovibles
#  de la aplicacion, es para evitar tener muchas tablas, 
# por ej: tipo documento, provincia, etc
#--------------------------------------------------  

class Parameter(models.Model):
    name = models.CharField(max_length=100)
    parameter_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @staticmethod
    def parameter_list(parameter_filter):
        return Parameter.objects.filter(parameter_type=parameter_filter)

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
    image = models.ImageField(
        upload_to=book_image_upload_to,
        storage=book_image_storage,
        blank=True,
        null=True
    )    
    status = models.ForeignKey(Parameter, on_delete=models.PROTECT,
                            limit_choices_to={'parameter_type': 'book_status'})
    aquisition_date = models.DateTimeField(default=timezone.now)
    user_booking = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='books_reserved',
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Book.objects.get(pk=self.pk)
            except Book.DoesNotExist:
                old_instance = None

            if old_instance and old_instance.image and old_instance.image != self.image:
                old_instance.image.delete(save=False)

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=True)
        return super().delete(*args, **kwargs)



