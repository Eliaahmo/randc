from django.contrib import admin
from .models import mitarbeiter
from .models import feedbackItem
from .models import feedbackGeber
from django.contrib.admin.sites import AdminSite 

AdminSite.site_header = "Systemverwaltung"
AdminSite.site_title = "Systemverwaltung"
AdminSite.index_title = "Willkommen in der Systemverwaltung"



class MitarbeiterAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'name', 'initial')  

admin.site.register(mitarbeiter, MitarbeiterAdmin)

class FeedbackItemAdmin(admin.ModelAdmin):
    #readonly_fields = [field.name for field in feedbackItem._meta.fields]  # Alle Felder als schreibgeschützt markieren

    #def has_add_permission(self, request):
      #  return False  # Das Hinzufügen neuer Einträge verhindern

    #def has_delete_permission(self, request, obj=None):
     #   return False  # Das Löschen von Einträgen verhindern
    list_display = ('created_at', 'category', 'grading', 'person', 'comment')  

admin.site.register(feedbackItem, FeedbackItemAdmin)

class FeedbackGeberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','angemeldet', 'bewertet')
admin.site.register(feedbackGeber, FeedbackGeberAdmin)
