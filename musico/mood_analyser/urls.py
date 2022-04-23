from django.urls import path
from .views import (
    MoodDetector
)

urlpatterns = [
    path('get_mood', MoodDetector.as_view(), name="get_mood"),
]