from PIL import Image
from pillow_heif import register_heif_opener
import glob
import os

dir_name = "jpgimg"

if not os.path.isdir(f"./{dir_name}"):
    os.mkdir(dir_name)

register_heif_opener()

# get all image name
images_list = glob.glob("*.heic")

for image in images_list:
    # set image name
    image_name= f"{dir_name}/{str(image)[:-5]}.jpg"
    # Open HEIF or HEIC file
    image = Image.open(image)
    # Convert to JPEG
    image.save(image_name)