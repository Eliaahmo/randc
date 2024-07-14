from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import feedbackItem, mitarbeiter, Fragenkatalog, feedbackGeber
from django.shortcuts import redirect
from django.db.utils import IntegrityError
from .forms import MitarbeiterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import feedbackGeber
from django.contrib.auth.hashers import check_password
import re
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
import pandas as pd
from .utils import get_cleaned_feedback_data
from django.db.models import Avg
import math

# Überprüfen, ob der Benutzer ein Administrator ist
def admin_or_partner_check(user):
    return user.is_superuser or user.partner

@login_required
@user_passes_test(admin_or_partner_check)
def feedback_overview(request):
    persons = feedbackItem.objects.values_list('person', flat=True).distinct()

    person_filter = request.GET.get('person')
    if person_filter:
        filtered_feedback_data = feedbackItem.objects.filter(person=person_filter)
    else:
        filtered_feedback_data = feedbackItem.objects.all()

    categories = filtered_feedback_data.values_list('category', flat=True).distinct()
    category_avg_grades = {}
    for category in categories:
        avg_grade = filtered_feedback_data.filter(category=category).aggregate(avg_grade=Avg('grading'))['avg_grade']
        category_avg_grades[category] = avg_grade if avg_grade is not None else 0.0

    total_avg_grade = filtered_feedback_data.aggregate(avg_grade=Avg('grading'))['avg_grade']

    # Laden Sie die Kategorien aus dem Modell Category
    fragen = Fragenkatalog.objects.all()
    fragen_list = list(fragen)

    # Erstellen Sie eine Liste von Tupeln (Frage, Durchschnittliches Grading)
    fragen_avg_grades = []
    for index, frage in enumerate(fragen_list):
        category_name = f"Kategorie {index + 1}"
        avg_grade = category_avg_grades.get(category_name, 0.0)
        fragen_avg_grades.append((frage.name, avg_grade))

    context = {
        'persons': persons,
        'filtered_feedback_data': filtered_feedback_data,
        'category_avg_grades': category_avg_grades,
        'total_avg_grade': total_avg_grade if total_avg_grade is not None else 0.0,
        'selected_person': person_filter if person_filter else 'Alle',
        'fragen_avg_grades': fragen_avg_grades
    }

    return render(request, 'feedback_overview.html', context)

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


def custom_login_view(request):
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        password = request.POST['password']

        # Benutzer authentifizieren
        user = authenticate(username=benutzername, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)  

                # Überprüfen, ob der Benutzer Superuser/Administrator/ Partner ist
                if user.is_superuser or user.partner:
                    feedbackgeber = feedbackGeber.objects.get(username=user.username)
                    if feedbackgeber.angemeldet == False:
                        feedbackgeber.angemeldet = True
                        feedbackgeber.save()

                    return redirect('feedback_overview')             

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
                    return render(request, '403.html')

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