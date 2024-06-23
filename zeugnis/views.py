from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import feedbackItem, mitarbeiter
from django.shortcuts import redirect
from django.db.utils import IntegrityError
from .forms import MitarbeiterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import feedbackGeber
from django.contrib.auth.hashers import check_password
import re
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    return render(request, 'login.html')

@csrf_exempt
@login_required
def bewertung_view(request):
    if request.method == 'POST':
        person = request.session.get('vorname', 'leer')  # Der bewertete Vorgesetzte
        success = True
        for i in range(1, 11):
            category = f'Kategorie {i}'
            print(category)
            grade = request.POST.get(f'k{i}')
            comment = request.POST.get(f'k{i}_comment')
            print(grade, comment)
            if grade:
                try:
                    feedbackItem.objects.create(
                        created_at=timezone.now().date(),
                        person=person,
                        category=category,
                        grading=int(grade),
                        comment = comment
                    )
                except IntegrityError as e:
                    print(f'Error saving category{i}: {e}')
                    success = False
        if success:

            return redirect('danke')  # Weiterleitung zur Dankeseite
        else:
            return render(request, 'zeugnis.html', {'error': 'Es gab einen Fehler beim Speichern der Bewertungen.'})

    return render(request, 'zeugnis.html')  # Dein bestehendes HTML-Formular

def danke(request):
    return render(request, 'danke.html')

@login_required
def mitarbeiter_erstellen(request):
    if not request.user.is_superuser:
        return render(request, '403.html')  # Render die benutzerdefinierte Fehlerseite
    
    if request.method == 'POST':
        form = MitarbeiterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mitarbeiter_erstellen')  # Ersetze 'success_page' durch den Namen deiner Erfolgsseite
    else:
        form = MitarbeiterForm()
    
    return render(request,'mitarbeiter_form.html', {'form': form})
  
def extract_initials(username):
    return ''.join(re.findall('[A-Za-z]', username))

@login_required
def zeugnis(request):
    return render(request, 'zeugnis.html')


def custom_login_view(request):
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        password = request.POST['password']

        print(f"Benutzername: {benutzername}, Passwort: {password}")  # Debug-Ausgabe

        # Benutzer authentifizieren
        user = authenticate(username=benutzername, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)  # Verwende auth_login anstelle von login

                # Initialen extrahieren und Mitarbeiter suchen
                initials = extract_initials(benutzername)
                try:
                    mitarbeiter_obj = mitarbeiter.objects.get(initial=initials)
                    vorname = mitarbeiter_obj.vorname
                except mitarbeiter.DoesNotExist:
                    vorname = "Person1"  # Standardwert, falls kein Mitarbeiter gefunden wurde

                # Speichern Sie den Vornamen in der Session
                request.session['vorname'] = vorname

                # Render die Bewertungsseite und übergib den Vornamen
                return render(request, 'zeugnis.html', {'vorname': vorname})
            else:
                return HttpResponse("Ihr Account ist nicht aktiv.")
        else:
            return HttpResponse("Ungültige Anmeldedaten.")

    return render(request, 'login.html')