from django.db import models
from datetime import date

# Create your models here.
class feedbackItem(models.Model):
    created_at = models.DateField(default = date.today)
    person = models.CharField(max_length=200, default = "leer")
    category = models.CharField(max_length = 1000)
    grading = models.SmallIntegerField(default = 0)

    def __str__(self):
        return f'{self.category} - {self.grade} für {self.person}'

class mitarbeiter(models.Model):
    vorname = models.CharField(max_length=200, default = "leer")
    name = models.CharField(max_length= 200, default = "leer")
    
