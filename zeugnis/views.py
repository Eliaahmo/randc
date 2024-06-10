from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import feedbackItem, mitarbeiter
from django.shortcuts import redirect
from django.db.utils import IntegrityError
from .forms import MitarbeiterForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.
def zeugnis(request):
    return render(request, 'zeugnis.html')

def login(request):
    return render(request, 'login.html')

@csrf_exempt
def bewertung_view(request):
    if request.method == 'POST':
        person = "leer"  # Der bewertete Vorgesetzte
        success = True
        for i in range(1, 11):
            category = f'Kategorie {i}'
            print(category)
            grade = request.POST.get(f'k{i}')
            print(grade)
            if grade:
                try:
                    feedbackItem.objects.create(
                        created_at=timezone.now().date(),
                        person=person,
                        category = category,
                        grading=int(grade)
                    )
                except IntegrityError as e:
                    print(f'Error saving category{i}: {e}')
                    success = False
        if success:

            return redirect('danke')  # Weiterleitung zur Dankeseite
        else:
            return render(request, 'zeugnis2.html', {'error': 'Es gab einen Fehler beim Speichern der Bewertungen.'})
            
    return render(request, 'zeugnis2.html')  # Dein bestehendes HTML-Formular

def zeugnis2(request):
    return render(request, 'zeugnis2.html')

def danke(request):
    return render(request, 'danke.html')

def mitarbeiter_erstellen(request):
    if request.method == 'POST':
        vorname = request.POST.get('vorname')
        name = request.POST.get('name')
        neuer_mitarbeiter = mitarbeiter.objects.create(
            vorname=vorname, name=name
            )
        neuer_mitarbeiter.save()
        print("Mitarbeiter hinzugefügt")
    return render(request, 'mitarbeiter_form.html')  # Das Formular anzeigen


@login_required
def mitarbeiter_erstellen2(request):
    if not request.user.is_superuser:
        return render(request, '403.html')  # Render die benutzerdefinierte Fehlerseite
    
    if request.method == 'POST':
        form = MitarbeiterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mitarbieter_form.html')  # Ersetze 'success_page' durch den Namen deiner Erfolgsseite
    else:
        form = MitarbeiterForm()
    
    return render(request, 'mitarbeiter_form.html', {'form': form})