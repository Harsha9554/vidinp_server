from io import FileIO
from os import path
import os
from urllib import response
from django.shortcuts import render, HttpResponse, redirect, Http404

from vidinp_server.settings import BASE_DIR
from .forms import ProcessForm, VideoForm
from .models import Video, ProcessedVideo
from .process import process_vid
from django.utils.encoding import smart_str



def index(request):
    if request.method == "POST":
        form = VideoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "index.html", {"form": form, "success": True})
    else:
        form = VideoForm()
    return render(request, "index.html", {"form": form, "success": False})

def actual(request):
    actual_vids = Video.objects.all()
    return render(request, "actual.html", {"actual_vids": actual_vids})



def pro(request):
    pro_vids = ProcessedVideo.objects.all()
    return render(request, "pro_all.html", {"pro_vids": pro_vids})
# def process(vid):
#     pass

def pro_with_id(request, id):
    actual_vid_id = id
    vid = Video.objects.get(id=actual_vid_id)
    vid.caption += "_pro"
    pro_vid_path = process_vid(vid)
    print(pro_vid_path)
    pro_vids = ProcessedVideo(id = actual_vid_id*10, caption = vid.caption, video = pro_vid_path)
    print("pro-saved.")
    pro_vids.save()
    file_path = "media/" + pro_vid_path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="video/mp4")
            response['Content-Disposition: attachment'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    # pro_vids = ProcessedVideo.objects.all()
    # return render(request, "pro_all.html", {"pro_vids": pro_vids})

# def is_pro_vid_valid(value):
#     file_size = value.size
#     if file_size == 0:
#         return False
#     return True


# def pro(request, id):
#     if request.method == "POST":
#         actual_id = id
#         actual_vid = Video.objects.filter(id=actual_id)
#         processed_vid = process_vid(actual_vid)
#         print(processed_vid.url)
#         print(type(processed_vid))
#         form = ProcessForm()
