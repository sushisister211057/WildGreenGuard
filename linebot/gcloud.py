from google.cloud import storage
from PIL import Image
import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"wildgreen-411520-37d993c760f1.json"


bucket_name = "green01"

#透過串流方式上傳圖片到Google Cloud Storage
async def upload_blob_from_stream(img, destination_blob_name): 
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # 將圖片轉換為位元（JPEG 格式）
    img_byte_arr = io.BytesIO()
    if isinstance(img, Image.Image):
        img.save(img_byte_arr, format="JPEG")
    if isinstance(img, bytes):
        img_byte_arr.write(img)
        
    # 取出位元值
    img_byte_arr = img_byte_arr.getvalue()

    blob.upload_from_string(img_byte_arr, content_type="image/jpeg")

    return blob.public_url

#下載物件(圖片)
# async def download_blob(img, source_blob_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(source_blob_name)

#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format='JPEG')
#     blob.download_blob(img_byte_arr, content_type="image/jpeg")

#     return blob.public_url