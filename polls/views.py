from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Video

# Create your views here.
def index(request):
    latest_video_list = Video.objects.order_by("-pub_data")[:5]
    context = {"latest_video_list": latest_video_list}
    # We don't need loader and HttpResponse with the render just like this
    return render(request, "polls/index.html", context)
    # return HttpResponse("Hello World!")

def video(request, video_name):
    try:
        _video = Video.objects.get(video_name=video_name)
    except Video.DoesNotExist:
        raise Http404("Does not exist")
    template = loader.get_template("polls/detail.html")
    context = {
        "videoInfo": _video.video_name
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're looking at %s." %video_name)

def videoUrl(request, video_name):
    # Don't use 'try' to catch the error, use get_object_or_404 to complete this.
    _video = get_object_or_404(Video, video_name=video_name)
    return render(request, "polls/detail.html", { "videoInfo": _video.video_url })
    