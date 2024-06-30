import pandas as pd
from .models import feedbackItem

def get_cleaned_feedback_data():
    feedback_data = feedbackItem.objects.all().values()
    df = pd.DataFrame(feedback_data)

    # Beispielhafte Bereinigungsoperationen
    df.fillna({'grading': 0}, inplace=True)
    df['comment'] = df['comment'].str.strip()

    return df