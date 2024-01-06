from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Plant

# Create your views here.

def index(request):
    """
    return image and inference or return upload button
    """
    if request.method == "POST":
        print("post")
        # print(request.FILES.get("image_input"))
        upload_img = request.FILES.get("image_input")
        data = {"image": upload_img, "species": "frog", "invasion": False}
        instance = Plant(**data)
        try: 
            instance.full_clean()
        except ValidationError as e:
            print(e.message_dict)

        instance.save()

        image = instance.image
        
        return render(request, "plants/index.html", {"image":image})

    else:
        return render(request, "plants/index.html")

    return HttpResponse("ok")

