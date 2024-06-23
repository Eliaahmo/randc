from django.db import models
from datetime import date
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser


# Create your models here.
class feedbackItem(models.Model):
    created_at = models.DateField(default = date.today)
    person = models.CharField(max_length=200, default = "leer")
    category = models.CharField(max_length = 1000)
    grading = models.SmallIntegerField(default = 0)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.category} - {self.grading} für {self.person} mit Kommentar {self.comment}'
    class Meta:
        verbose_name_plural = "Feedback Rückmeldungen"

class mitarbeiter(models.Model):
    vorname = models.CharField(max_length=200, default = "leer")
    name = models.CharField(max_length= 200, default = "leer")
    initial = models.CharField(max_length= 200, default = "leer")
    
    class Meta:
        verbose_name_plural = "mitarbeiter"

    def __str__(self):
        return self.vorname


'''class feedbackGeber(models.Model):
    benutzername = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    angemeldet = models.BooleanField(default=False)
    bewertet = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = "feedbackgeber"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
'''
class feedbackGeber(AbstractUser):
    angemeldet = models.BooleanField(default=False)
    bewertet = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)