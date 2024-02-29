import requests
import numpy as np
from PIL import Image
import io
from django.conf import settings


async def yolo_predict(input):
    """
    post image byte to yolo model for predicting

    input: byte of image
    """
    files = {"file": ("image", input, "image/jpeg")}
    res = requests.post(url=settings.YOLO_API_URL, files=files)

    # convert json to Image
    img_array = np.array(res.json()["result"],dtype=np.uint8)
    print(img_array.shape)
    im = Image.fromarray(img_array)
    im = im.convert("RGB")

    # convert Image to byte
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")  # Adjust the format as needed
    img_bytes = buffered.getvalue()

    return img_bytes