from django.urls import path

from . import views

urlpatterns = [
    # str int slug uuid path is available
    # slug Matches any slug string consisting of ASCII letters or numbers
    path("", views.index, name="index"),
    path("<str:video_name>/", views.video, name="video"),
    path("<str:video_name>/video_url", views.videoUrl, name="videoUrl")
]