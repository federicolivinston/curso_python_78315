import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def user_avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.user.id}.{ext}"
    return os.path.join('avatares', filename)

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=user_avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return f"Avatar de {self.user.username}"

    def save(self, *args, **kwargs):
        # pisar el archivo para que siempre haya uno
        try:
            old_avatar = Avatar.objects.get(pk=self.pk)
            if old_avatar.imagen and old_avatar.imagen != self.imagen:
                old_avatar.imagen.delete(save=False)
        except Avatar.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Borrar imagen física si existe
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super().delete(*args, **kwargs)    