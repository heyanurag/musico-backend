from django.urls import path
from .views import (
    MoodDetector,
    PopularMusicByMood,
    SearchTracks
)

urlpatterns = [
    path('get_mood', MoodDetector.as_view(), name="get_mood"),
    path('get_popular', PopularMusicByMood.as_view(), name="get_popular"),
    path('get_search_result', SearchTracks.as_view(), name="get_search_result"),
]