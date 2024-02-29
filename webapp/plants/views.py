import io
import logging
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage.filesystem import FileSystemStorage
from django.core.files.base import ContentFile
from .models import Plant
from .identifier import predictor
from .yolopredict import yolo_predict
from .lineapi import save_user_data, get_user_data


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

        # set global pre img path
        global pre_img
        if pre_img:
            fms.delete(pre_img)
        pre_img = cur_img

        settings.TRANS_DICT["image"] = path
        logging.debug(path)

        # create byte buffer for predict
        buffer = io.BytesIO()
        for chunk in upload_img.chunks(chunk_size=1024):
            buffer.write(chunk)
        buffer.seek(0)
        img_byte = buffer.read()
        
        # predict species and isinvasive 
        species, isinvasive = predictor(img_byte)

        species_name = settings.TRANS_DICT[species]
        settings.TRANS_DICT["species_name"] = species_name
        settings.TRANS_DICT["isinvasive"] = isinvasive

        # save data if user is autheticated
        if request.user.is_authenticated:
            # do save data
            userid = request.user.userid
            # save user im to gcs
            async_to_sync(save_user_data)(userid, img_byte, species, isinvasive)

        return render(request, "plants/identifier.html", settings.TRANS_DICT)

    else:
        settings.TRANS_DICT["species_name"] = "noinput"
        return render(request, "plants/identifier.html", settings.TRANS_DICT)


# return yolov8 present model
def yolo_identifier(request):

    if request.method == "POST":
        # prepare img url for display
        upload_img = request.FILES.get("image_input_yolo")  

        # create byte buffer for predict
        buffer = io.BytesIO()
        for chunk in upload_img.chunks(chunk_size=1024):
            buffer.write(chunk)
        buffer.seek(0)
        img_byte = buffer.read()

        # send image to yolo model
        result = async_to_sync(yolo_predict)(img_byte)

        # save result to storage
        fms = FileSystemStorage()
        cur_img = fms.save(upload_img.name, ContentFile(result))
        path = fms.url(cur_img)

        # set global pre img path
        global pre_img
        if pre_img:
            fms.delete(pre_img)
        pre_img = cur_img

        settings.TRANS_DICT["image_yolo"] = path
        logging.debug(path)

        return render(request, "plants/yolo_identifier.html", settings.TRANS_DICT)
    
    else:
        return render(request, "plants/yolo_identifier.html", settings.TRANS_DICT)

# set index
def index(request):
    logging.debug(f"index page : {request.user.is_authenticated}")
    return render(request, "plants/index.html", settings.TRANS_DICT)

# retrieve records
@login_required
def records(request):
    if request.method == "GET":
        userid = request.user.userid
        user_records = async_to_sync(get_user_data)(userid)
        user_records = user_records[0]["records"] # 要修正
        logging.debug(user_records)
        settings.TRANS_DICT["user_records"] = user_records
        return render(request, "plants/records.html", settings.TRANS_DICT)

# list all available species
def diagram(request):
    plants = Plant.objects.all()
    settings.TRANS_DICT["plants"] = plants
    return render(request, "plants/diagram.html", settings.TRANS_DICT)

# list all developers
def developer(request):
    return render(request, "plants/developers.html", settings.TRANS_DICT)

# list all frequent asked questions
def freq_question(request):
    return render(request, "plants/freq_questions.html", settings.TRANS_DICT)

# href for changing language mode
def lan_mode(request):
    # language, source path, line userid
    if request.method == "GET":
        mode = request.GET.get("mode", default= "chi")
        next = request.GET.get("next", default= "index")

        # set lan_mode value
        request.session["lan_mode"] = mode

        return redirect(next)