import csv
from django.core.management.base import BaseCommand
from zeugnis.models import feedbackItem

class Command(BaseCommand):
    help = 'Export feedback items as CSV'

    def handle(self, *args, **kwargs):
        # Dateinamen für den CSV-Export festlegen
        file_path = 'feedback_export.csv'

        # Feedback-Items aus der Datenbank abrufen
        feedback_items = feedbackItem.objects.all()

        # CSV-Datei öffnen und schreiben
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            # Header schreiben
            writer.writerow(['ID', 'Created At', 'Person', 'Category', 'Grading', 'Comment'])
            # Daten schreiben
            for item in feedback_items:
                writer.writerow([item.id, item.created_at, item.person, item.category, item.grading, item.comment])

        self.stdout.write(self.style.SUCCESS(f'Successfully exported feedback items to {file_path}'))