from django.contrib import admin
from .models import mitarbeiter

class MitarbeiterAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'name', 'initial')  

admin.site.register(mitarbeiter, MitarbeiterAdmin)

