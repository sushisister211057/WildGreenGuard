from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Plant
from pathlib import Path
import json
from .lineapi import save_user_data
from django.template import loader
from asgiref.sync import async_to_sync
# Create your views here.


def identifier(request):
    """
    return image and inference or return upload button
    """
    if request.method == "POST":
        print("post")
        # print(request.FILES.get("image_input"))
        upload_img = request.FILES.get("image_input")
        
        data = {"imgurl": upload_img, "scientific_name": "frog", "isinvasive": False}
        instance = Plant(**data)
        try: 
            instance.full_clean()
        except ValidationError as e:
            print(e.message_dict)

        instance.save()

        settings.TRANS_DICT["image"] = instance.imgurl

        if request.user.is_authenticated:
            # do save data
            userid = request.user.userid
            # await 
            # async_to_sync(save_user_data(userid))
            pass
        
        return render(request, "plants/identifier.html", settings.TRANS_DICT)

    else:
        return render(request, "plants/identifier.html", settings.TRANS_DICT)


# return yolov8 present model
def rt_identifier(request):
    pass

# set index
def index(request):
    return render(request, "plants/index.html", settings.TRANS_DICT)

# retrieve records
@login_required
def records(request):
    return render(request, "plants/records.html", settings.TRANS_DICT)

# list all available species
def diagram(request):
    pass

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