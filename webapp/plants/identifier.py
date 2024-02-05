import requests
from PIL import Image
import numpy as np
import io
import json
from .models import Plant
from django.conf import settings

size = settings.IM_SIZE
names = [(obj["scientific_name"], obj["isinvasive"]) for obj in \
         Plant.objects.order_by("scientific_name").values("scientific_name", "isinvasive")]

def preditor(img_byte):
    instance = preprocessing(img_byte)
    
    data = json.dumps({
        "instances": instance
    })
    
    res = requests.post(settings.TF_SERVE_URL, data=data)
    print(res.json())
    predictions = res.json()["predictions"]
    print(predictions)
    idx = np.argmax(predictions, axis=1)

    # species, isinvasive = names[idx]
    
    # return species, isinvasive

def preprocessing(img_byte):
    im = Image.open(io.BytesIO(img_byte))
    im = im.convert("RGB")
    im = im.resize((size, size))
    tensor =  np.expand_dims(np.asarray(im), axis=0)
    instance = tensor.tolist()
    return instance