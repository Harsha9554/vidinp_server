from django.shortcuts import render, HttpResponse, redirect
from .forms import ProcessForm, VideoForm
from .models import Video, ProcessedVideo
from .process import process_vid


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
    pro_vid = process_vid(vid)
    print(type(pro_vid))
    # pro_vid = ProcessedVideo.objects.create_pro(id = actual_vid_id*10, caption = vid.caption, video = vid.video)
    # print("pro-saved.")
    # # pro_vid.save()
    return render(request, "pro.html", {"pro": pro_vid})

# def is_pro_vid_valid(value):
#     file_size = value.size
#     if file_size == 0:
#         return False
#     return True


# def pro(request, id):
#     if request.method == "POST":
#         actual_id = id
#         actual_vid = Video.objects.filter(id=actual_id)
#         processed_vid = process(actual_vid)
#         form = ProcessForm()
