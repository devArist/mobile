from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Base(models.Model):
    date_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date d'ajout"
        )
    date_update = models.DateTimeField(
        auto_now=True,
        verbose_name="dernière modification"
        )
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Contact(Base):
    name = models.CharField(max_length=200, verbose_name='nom')
    email = models.EmailField(max_length=254, blank=True, null=True)
    phonenumber = models.CharField(max_length=15, verbose_name='téléphone')
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="utilisateur", 
        on_delete=models.CASCADE,
        related_name='contacts',
        null=True
        )

    def __str__(self):
        return self.name


class Note(Base):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="utilisateur", 
        on_delete=models.CASCADE,
        related_name='notes',
        null=True
        )

    def __str__(self):
        return self.title