from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Plant, Record

# Create your views here.

def identifier(request):
    """
    return image and inference or return upload button
    """
    if request.method == "POST":
        print("post")
        # print(request.FILES.get("image_input"))
        upload_img = request.FILES.get("image_input")
        
        data = {"image": upload_img, "species": "frog", "invasion": False}
        instance = Record(**data)
        try: 
            instance.full_clean()
        except ValidationError as e:
            print(e.message_dict)

        instance.save()

        image = instance.image
        
        return render(request, "plants/identifier.html", {"image":image})

    else:
        return render(request, "plants/identifier.html")

    return HttpResponse("ok")

# return yolov8 present model
def rt_identifier(request):
    pass

# set index
def index(request):
    return render(request, "plants/index.html")

# retrieve records
def records(request):
    pass

# list all available species
def plants(request):
    pass

# list all developers
def developer(request):
    return render(request, "plants/developers.html")

# list all frequent asked questions
def freq_question(request):
    return render(request, "plants/freq_questions.html")