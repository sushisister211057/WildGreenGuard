import numpy as np
from db import get_distinct_plant
from PIL import Image
import aiohttp
import configparser


SIZE = 360

# 帶入config.ini檔案裏面的資訊
config = configparser.ConfigParser()
config.read("config.ini")

url = config.get("tensorflow", "url")


# img: Image
async def identifier(img:Image):
    # 對圖片進行預處理
    input_img = await preprocessing(img)
    # 準備要傳送給模型的資料(型別為列表)
    data = {
        "instances": input_img.tolist(),
    } 
  # Your API endpoint
    # 使用 aiohttp 客戶端建立連線，將預處理後的圖片資料送到指定的 API 端點
    async with aiohttp.ClientSession() as session:
        res = await session.post(url=url, json=data)
        result = await res.json()
        
        predictions = result["predictions"]
    # result = model.predict(resized_img) 
    # if np.max(predictions, axis=1) < 0.5: # [[0.1, 0.2, 0.3]]
    #     return 'other', None
    # 從模型預測結果中取得最有可能的植物種類索引
    idx = np.argmax(predictions, axis=1)
   
    # 根據索引取得植物種類和是否具侵入性
    species, isinvasive = get_distinct_plant(int(idx[0])).values()
    return species, isinvasive

# 對圖片進行預處理
async def preprocessing(img: Image):
    # 調整圖片大小至指定尺寸(360 x 360)
    resize_img = img.resize((SIZE, SIZE))
    # 轉換圖片為 NumPy 陣列，並將數值轉換為 0 到 1 之間的浮點數
    array = np.array(resize_img, dtype="float32")
    array = array / 255.0
    # 在陣列的第一維度上增加一個維度，以符合tensorflow模型輸入的格式(四維)
    input_img = np.expand_dims(array, axis=0)
    
    return input_img

# 向tensorflow模型的 REST API 端點發送預測請求
# async def predict_rest(input_img, json_data, url):
#     data = {
#         "instances": input_img.tolist(),
#     }  # Your JSON data
 
#     # 使用 POST 方法向 API 端點發送 JSON 格式的預測請求
#     async with aiohttp.ClientSession() as session:
#         res = await session.post(url=url, json=json_data)
#         # 從 API 回傳的響應中取得 JSON 格式的預測結果
#         result = await res.json()
#         print(res.status)
#         return result
    



