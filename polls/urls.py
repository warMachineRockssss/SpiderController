from django.urls import path

from . import views

urlpatterns = [
    # str int slug uuid path is available
    # slug Matches any slug string consisting of ASCII letters or numbers
    path("", views.index, name="index"),
    path("submit_url/", views.handleUrl, name="handleUrl"),
    path("<str:video_name>/", views.video, name="video"),
    path("<str:video_name>/video_url", views.videoUrl, name="videoUrl"),
    path("spider/<str:spider_name>", views.runspider, name="runspider"),
]