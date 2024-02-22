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
from asgiref.sync import async_to_sync, sync_to_async
from PIL import Image
import hashlib
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
        im = Image.open(buffer)
        print(type(img_byte), type(im))
        
        species, isinvasive = preditor(img_byte)

        settings.TRANS_DICT["species"] = species
        settings.TRANS_DICT["isinvasive"] = isinvasive

        # save data if user is autheticated
        if request.user.is_authenticated:
            # do save data
            userid = request.user.userid
            # save user im to gcs
            print(userid)
            async_to_sync(save_user_data)(userid, img_byte, species, isinvasive)

        return render(request, "plants/identifier.html", settings.TRANS_DICT)

    else:
        return render(request, "plants/identifier.html", settings.TRANS_DICT)


# return yolov8 present model
def rt_identifier(request):
    pass

# hash_user = hashlib.sha256("userid".encode("utf-8")).hexdigest()
# request.session[hash_user] = "123"
# key = request.session.get(hash_user)
# print(key)
# userid = request.user.userid
# userid = "Uea2325d897976dda7912258a6aa1abe3"
# user_data = async_to_sync(get_user_data)(userid)
# print(user_data)
# print([name for _, name in [Plant.objects.order_by("scientific_name").values("scientific_name")]])

# set index
def index(request):
    print("index", request.user.is_authenticated)
    return render(request, "plants/index.html", settings.TRANS_DICT)

# retrieve records
@login_required
def records(request):
    if request.method == "GET":
        userid = request.user.userid
        user_records = async_to_sync(get_user_data)(userid)
        print(type(user_records))
        user_records = user_records[0]["records"]
        settings.TRANS_DICT["user_records"] = user_records
        return render(request, "plants/records.html", settings.TRANS_DICT)

# list all available species
def diagram(request):
    plants = Plant.objects.all()
    settings.TRANS_DICT["plants"] = plants
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
        mode = request.GET.get("mode", default= "chi")
        next = request.GET.get("next", default= "index")

        # set lan_mode value
        request.session["lan_mode"] = mode

        return redirect(next)