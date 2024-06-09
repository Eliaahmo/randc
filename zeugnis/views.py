from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import feedbackItem
from django.shortcuts import redirect
from django.db.utils import IntegrityError

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