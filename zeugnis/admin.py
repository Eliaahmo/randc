from django.contrib import admin
from .models import mitarbeiter
from .models import feedbackItem
from .models import feedbackGeber
from .models import Fragenkatalog
from django.contrib.admin.sites import AdminSite 

AdminSite.site_header = "Systemverwaltung"
AdminSite.site_title = "Systemverwaltung"
AdminSite.index_title = "Willkommen in der Systemverwaltung"



class MitarbeiterAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'name', 'initial') 
    search_fields = ('vorname', 'name', 'initial') 

admin.site.register(mitarbeiter, MitarbeiterAdmin)

class FeedbackItemAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in feedbackItem._meta.fields]  # Alle Felder als schreibgeschützt markieren

    def has_add_permission(self, request):
        return False  # Das Hinzufügen neuer Einträge verhindern

    def has_delete_permission(self, request, obj=None):
        return False  # Das Löschen von Einträgen verhindern
    
    def has_change_permission(self, request, obj=None):
        return False
    
    list_display = ('created_at', 'category', 'grading', 'person', 'comment')  
    search_fields = ('person', 'category', 'comment','created_at')

admin.site.register(feedbackItem, FeedbackItemAdmin)

class FeedbackGeberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','angemeldet', 'bewertet','partner')
    search_fields = ('username', 'email','angemeldet','bewertet','partner')
admin.site.register(feedbackGeber, FeedbackGeberAdmin)

class FragenkatalogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Fragenkatalog, FragenkatalogAdmin)