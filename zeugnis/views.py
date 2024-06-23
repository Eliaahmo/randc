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
            # Setzen Sie das 'bewertet'-Attribut des aktuellen Benutzers auf True
            current_user = feedbackGeber.objects.get(username=request.user.username)
            current_user.bewertet = True
            current_user.save()
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


'''def custom_login_view(request):
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

    '''

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

                # Überprüfen, ob der Benutzer Superuser/Administrator ist
                if user.is_superuser:
                    return handle_login_success(request, user)

                # Initialen extrahieren und Mitarbeiter suchen
                initials = extract_initials(benutzername)
                try:
                    mitarbeiter_obj = mitarbeiter.objects.get(initial=initials)
                    vorname = mitarbeiter_obj.vorname
                except mitarbeiter.DoesNotExist:
                    vorname = "Person1"  # Standardwert, falls kein Mitarbeiter gefunden wurde

                # Speichern Sie den Vornamen in der Session
                request.session['vorname'] = vorname

                # Überprüfen, ob der Benutzer bereits angemeldet und bewertet hat
                try:
                    feedbackgeber = feedbackGeber.objects.get(username=user.username)
                    if feedbackgeber.angemeldet and feedbackgeber.bewertet:
                        return render(request, '404.html')
                    elif feedbackgeber.angemeldet and not feedbackgeber.bewertet:
                        # Benutzer hat sich bereits angemeldet, aber noch keine Bewertung abgegeben
                        return render(request, 'zeugnis.html', {'vorname': vorname})
                    else:
                        # Benutzer hat sich noch nicht angemeldet
                        feedbackgeber.angemeldet = True
                        feedbackgeber.save()
                except feedbackGeber.DoesNotExist:
                    # Neuer Benutzer, der sich zum ersten Mal anmeldet
                    feedbackGeber.objects.create(username=user.username, angemeldet=True)

                # Render die Bewertungsseite und übergib den Vornamen
                return render(request, 'zeugnis.html', {'vorname': vorname})
            else:
                return HttpResponse("Ihr Account ist nicht aktiv.")
        else:
            return render(request, '403.html')

    return render(request, 'login.html')

def handle_login_success(request, user):
    # Render hier die Seite nach dem erfolgreichen Login
    return render(request, 'zeugnis.html', {'user': user})