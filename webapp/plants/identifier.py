import requests
from PIL import Image
import numpy as np
import io
import json
from .models import Plant
from django.conf import settings

size = settings.IM_SIZE
names = []

def predictor(img_byte):
    instance = preprocessing(img_byte)
    
    data = json.dumps({
        "instances": instance
    })
    
    res = requests.post(settings.TF_SERVE_URL, data=data)
    predictions = res.json()["predictions"]
    idx = np.argmax(predictions, axis=1)[0]
    
    global names
    if not names:
        names = [(obj["scientific_name"], obj["isinvasive"]) for obj in \
        Plant.objects.order_by("scientific_name").values("scientific_name", "isinvasive")]

    species, isinvasive = names[int(idx)]

    return species, isinvasive

def preprocessing(img_byte):
    im = Image.open(io.BytesIO(img_byte))
    im = im.convert("RGB")
    im = im.resize((size, size))
    tensor =  np.expand_dims(np.asarray(im), axis=0)
    instance = tensor.tolist()
    return instance