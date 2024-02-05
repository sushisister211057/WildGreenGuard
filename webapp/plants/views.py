from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage.filesystem import FileSystemStorage
from .models import Plant
from pathlib import Path
from .identifier import preditor
import json
import io
from .lineapi import save_user_data, get_user_data
from django.template import loader
from asgiref.sync import async_to_sync
# Create your views here.

pre_img = ""

def identifier(request):
    """
    return image and inference or return upload button
    """
    if request.method == "POST":
        # prepare img url for display
        upload_img = request.FILES.get("image_input")
        fms = FileSystemStorage()
        cur_img = fms.save(upload_img.name, upload_img)
        path = fms.url(cur_img)

        # set global
        global pre_img
        if pre_img:
            fms.delete(pre_img)
        pre_img = cur_img

        settings.TRANS_DICT["image"] = path
        print(path)

        # wait for delete
        # data = {"imgurl": upload_img, "scientific_name": "frog", "isinvasive": False}
        # instance = Plant(**data)
        # try: 
        #     instance.full_clean()
        # except ValidationError as e:
        #     print(e.message_dict)

        # create byte buffer for predict
        buffer = io.BytesIO()
        for chunk in upload_img.chunks(chunk_size=1024):
            buffer.write(chunk)
        buffer.seek(0)
        img_byte = buffer.read()
        print(type(img_byte))
        
        species, isinvasive = preditor(img_byte)
        # save data if user is autheticated
        if request.user.is_authenticated:
            # do save data
            userid = request.user.userid
            async_to_sync(save_user_data)(userid, img_byte, species)
        
        return render(request, "plants/identifier.html", settings.TRANS_DICT)

    else:
        return render(request, "plants/identifier.html", settings.TRANS_DICT)


# return yolov8 present model
def rt_identifier(request):
    print([(obj["scientific_name"], obj["isinvasive"]) for obj in \
         Plant.objects.order_by("scientific_name").values("scientific_name", "isinvasive")])
    pass

# set index
def index(request):
    return render(request, "plants/index.html", settings.TRANS_DICT)

# retrieve records
@login_required
def records(request):
    if request.method == "GET":
        pass

    if request.method == "POST":
        data = request.POST

    return render(request, "plants/records.html", settings.TRANS_DICT)

# list all available species
def diagram(request):
    # userid = request.user.userid
    userid = "U3dcfb815c81a9428865e4ed5d257c4cc"
    user_data = async_to_sync(get_user_data)(userid)
    print(user_data)
    # print([name for _, name in [Plant.objects.order_by("scientific_name").values("scientific_name")]])
    return render(request, "plants/diagram.html", settings.TRANS_DICT)

# list all developers
def developer(request):
    print(request.user)
    return render(request, "plants/developers.html", settings.TRANS_DICT)

# list all frequent asked questions
def freq_question(request):
    return render(request, "plants/freq_questions.html", settings.TRANS_DICT)


def lan_mode(request):
    # language, source path, line userid
    if request.method == "GET":
        code = request.GET.get("code", default= "chi")
        next = request.GET.get("next", default= "index")

        # set lan_mode value
        request.session["lan_mode"] = code

        return redirect(next)