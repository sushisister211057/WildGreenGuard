import uvicorn
from fastapi import FastAPI, Request
import json
import requests
import configparser
import aiohttp
from db import save_record,get_user_records, get_species_records, get_plants, get_all_records
from datetime import datetime
from PIL import Image
import io
from identifier import identifier
import time
from gcloud import upload_blob_from_stream
import redis
import logging

# FastAPI
app = FastAPI()

# 將logging級別設置為DEBUG
logging.basicConfig(level="DEBUG")


# 帶入config.ini檔案裏面的資訊
config = configparser.ConfigParser()
config.read("config.ini")

# 標頭
headers= {
    "Content-type": "application/json",
    "Authorization": f"Bearer {config.get('line-bot', 'channel_access_token')}"
}

# 帶入config.ini檔案裏面網頁的資訊
web_dns = config.get("web", "web_dns")
base_url = config.get("web", "base_url")
csrf_url = config.get("web", "csrf_url")
access_token_url = config.get("web", "access_token_url")

# redis連線
redis_host = config.get("redis", "host")
redis_port = config.getint("redis", "port")
r= redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
if r.ping():
    logging.info(f"Pinged your deployment. You successfully connected to Redis!")


# 讀取translate.json裡面的內容轉換為字典形式(初始為空字典)
trans_dict_repo = {}
# translate.json裡面的翻譯內容(初始為空字典)
trans_dict = {}


# Fast API 讀取
@app.get("/")
def getinfo():
    return "ok"

# Fast API 發送
@app.post("/")
async def index(request: Request):
    # 從請求(request)中讀取JSON格式的內容
    logging.debug(await request.body())

    # 取得headers裡面的content_type 
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        body = await request.json()
    
    # 取得網頁端傳的payload跟image
    elif "multipart/form-data" in content_type:
        form = await request.form()
        body = json.loads(form.get("payload"))
        file = form.get("image")
        img = await file.read()

    # 從JSON內容中提取名為"events"的鍵對應的值
    events = body["events"]

    # 連線webhook偵測用
    if len(events) == 0:
        return "ok"

    # 取得userid
    userid = events[0]["source"]["userId"]

    
    # 回覆訊息，訊息內容預設為空列表
    if "replyToken" in events[0]:

        # 使用者加入Line bot(必須在語言切換前)
        if events[0]["type"] == "follow":
            return "new user"

        # 套用目前設定語言
        await get_trans_dict(userid)

        replyToken = events[0]["replyToken"]
        payload={
            "replyToken" : replyToken,
            "messages" :[]
        }
        
        # 型別為postback，取出postback裡面的data
        if events[0]["type"] == "postback":
            data = events[0]["postback"]["data"]

            # 外來種植物辨識功能-上傳一張植物圖片，附有上傳圖片及開啟相機的功能
            if data == "idplant":
                payload["messages"].append(await upload_image())
            
            # 外來種植物辨識辨識失敗不再辨識的回覆內容
            elif data == trans_dict["thxuse"]:
                payload["messages"]= [await thx_use_msg()]

            # 根據圖文選單所選擇的語言，以相應的語言回覆訊息
            elif data in ["richmenu-changed-to-chinese", "richmenu-changed-to-english", "richmenu-changed-to-japanese"]:
                match data:
                    case "richmenu-changed-to-chinese":
                        await get_trans_dict(userid, mode="chi")
                    case "richmenu-changed-to-english":
                        await get_trans_dict(userid, mode="en")
                    case "richmenu-changed-to-japanese":
                        await get_trans_dict(userid, mode="jp")
                return "change language done"
            
            # 網頁功能- 傳送userid, 使用者名稱, source到網頁端，並顯示quick reply(立即前往、登入資訊)
            elif data == "weblog":
                display_name = await get_user_name(userid)
                uri = await login_info(userid, display_name)
                payload["messages"]= [
                    await quick_reply(text=trans_dict["weblog"], actions=[
                        {"action_type":"uri", "label":trans_dict["visweb"], "uri": uri},
                        {"action_type":"postback", "label":trans_dict["loginfo"], "data": "credential"}
                        ])]
            
            # 顯示網頁登入資訊: userid(前7碼)、使用者名稱
            elif data == "credential": 
                display_name = await get_user_name(userid)
                payload["messages"] = [
                    {"type": "text" , "text": f"{trans_dict['id']} : {userid[:7]}\n{trans_dict['username']}: {display_name}"}
                ]

            # 歷史紀錄查詢回覆內容:好好欣賞植物圖片吧!
            elif data == "enjimg":
                payload["messages"].append(await view_image_info())

            # 歷史紀錄查詢點選圖片旋轉木馬選單後出現使用者拍攝的圖片
            elif data[8:15] == "storage":
                payload["messages"]= [await share_img(data)]

            # 歷史紀錄查詢回覆內容:點選上方的「查看更多資訊」吧!
            elif data == "clvimgin":
                payload["messages"].append(await click_view_info())

            # 歷史紀錄查詢功能的data
            else: 
                data = json.loads(data)
                action = data["action"]
                skip = data["skip"]

                # 旋轉木馬選單歷史紀錄(Mongodb)
                if action == "search":
                    user_records = get_user_records(userid, skip)

                    # 沒有歷史紀錄的回覆:沒有任何歷史紀錄喔!
                    if not user_records:
                        payload["messages"].append({
                            "type": "text",
                            "text" : trans_dict["norec"]
                    })
                        
                    # 歷史紀錄查詢quick reply:是否再顯示其他的植物種類?
                    else:   
                        payload["messages"]= [
                            await get_history(user_records, data),
                            await quick_reply(text=trans_dict["disother"], actions=[
                                {"action_type":"postback", "label":trans_dict["y"], "data": json.dumps({"action": action, "skip": skip + 10})},
                                {"action_type":"postback", "label":trans_dict["n"], "data": "clvimgin"}])]
                        
                # 圖片旋轉木馬選單歷史紀錄(Mongodb)
                else:
                    species = data["species"]
                    records = get_species_records(userid, species, skip)

                    # 歷史紀錄植物物種小於10種的回覆:目前歷史紀錄裡只有上面的植物種類喔！
                    if not records:
                        payload["messages"].append({
                                "type": "text",
                                "text" : trans_dict["curhis"]
                        })

                    # 不再查看先前的歷史紀錄回覆:好好欣賞植物圖片吧!
                    else:
                        payload["messages"]= [await display_history(records),
                                          await quick_reply(text=trans_dict["prehis"], actions=[
                            {"action_type":"postback", "label":trans_dict["y"], "data": json.dumps({"action": action, "species": species, "skip": skip + 5})},
                            {"action_type":"postback", "label":trans_dict["n"], "data": "enjimg"}])]
            await reply_message(payload)

        # 型別為message
        elif events[0]["type"] == "message":
             if events[0]["message"]["type"] == "image":

                # 取得圖片id
                img_id = events[0]["message"]["id"]

                img = await get_upload_image(img_id)
                
                # 避免使用者一次上傳多張圖片進行辨識
                current_time = time.time()
                previous_time = 0 if not r.hget(name=userid, key="last_img_time") else r.hget(name=userid, key="last_img_time")
                r.hset(name=userid, key="last_img_time", value=current_time)

                if current_time - float(previous_time) < 3:
                    return 
                

                # 導入模組辨別植物名稱跟是否為外來種(identifier.py)
                species, isinvasive = await identifier(img)
                # species = "other" #測試retry_confirm
                # isinvasive = "False" #測試retry_confirm
                logging.debug(f"result: {species}, {isinvasive}")
                # species = "other"
                # if species in plants -> save 如果是符合辨識的植物種類就儲存
                if species != "other":
                    # save record
                    # image -> upload img -> img url -> mongodb
                    # 儲存圖片到 GCP storage (gcloud.py)
                    img_url = await upload_blob_from_stream(img, f"record/{userid[:7]}/img_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
                    save_record(species, img_url, datetime.now(), userid, isinvasive)
                    # 辨別植物成功的回覆訊息
                    payload["messages"].append(await identify_success(species, userid))
                   
                # 辨別植物失敗的回覆訊息
                else:
                    payload["messages"]=[
                        await identify_fail(),
                        await retry_confirm()
                    ]
                await reply_message(payload)
            
    # for web login user 
    else:
        is_species = events[0].get("species", False)
        # save user record (儲存使用者紀錄)
        if is_species:
            species = events[0]["species"]
            isinvasive = events[0]["isinvasive"]
            
            img_url = await upload_blob_from_stream(img, f"record/{userid[:7]}/img_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
            save_record(species, img_url, datetime.now(), userid, isinvasive)
            
            return "save done"
        
        # get all user records (取得使用者的所有歷史紀錄)
        else:
            userdata = get_all_records(userid) # 測試MongoDB內容格式
            return userdata
        
    return "ok"        


# 回覆訊息
async def reply_message(payload: dict) -> str:
    url = "https://api.line.me/v2/bot/message/reply"
    async with aiohttp.ClientSession() as session:
        res = await session.post(url=url, headers=headers, json=payload)
        logging.debug(f"reply: {res.status}")
        # print("reply",await res.json())
        # print(res.text)
    return "ok"

# 將translate.json裡的內容載入到全域變數 trans_dict_repo
async def set_language_repo() -> str:
    global trans_dict_repo
    with open("translate.json","r", encoding="utf-8") as f :
        text_open = f.read()
        trans_dict_repo = dict(json.loads(text_open))
    return "done"

# 根據指定的語言模式，從全域變數 trans_dict_repo 中提取相應的語言詞彙
# **kwargs目前只用在userid
async def get_trans_dict(userid: str, **kwargs) -> str:
    # key : [中文0, 英文1, 日文2]
    lan_int = {"chi": 0, "en": 1, "jp": 2}

    global trans_dict_repo
    # 如果翻譯字典尚未被設定，則呼叫 set_language_repo() 函數進行設定
    if not trans_dict_repo:
        await set_language_repo()
        
    # 從kwargs取出語言mode
    mode = "" if not kwargs.get("mode") else kwargs.get("mode") 
    # 如果未指定語言模式，則通過Line API獲取用戶的richMenuId設定語言

    if not mode:
        mode = await language(userid)  

    # 語言模式暫存到redis
    r.hset(name=userid, key="mode", value=mode)

    logging.debug(f"language: {mode}")

    global trans_dict
    
    # 使用字典生成式建立 trans_dict 字典，選擇對應語言模式的翻譯
    trans_dict = {key : value[lan_int[mode]] for key, value in trans_dict_repo.items()}

    return "ok"


# 依據richmenuid設定語言
async def language(userid: str) -> str: 
    
    # 從Redis暫存中取語言模式
    mode = r.hget(name=userid, key="mode")
    if mode:
        return mode
    
    lan_id = {"richmenu-8efd417031f98d85d6b31a7e092db9a8": "chi",
              "richmenu-08b61ee74ee84ed6a99cda1ea9537ee5": "en", 
              "richmenu-f06501417699e11acd495b56df9e77ed": "jp"}
    
    url = f"https://api.line.me/v2/bot/user/{userid}/richmenu"
        # 使用 aiohttp 客戶端建立連線，發送 GET 請求
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            res = await response.json()
            # print(res["richMenuId"])
            # 根據回傳的 richMenuId 取得對應的語言模式
            mode = lan_id[res["richMenuId"]]

    return mode

# 取得使用者上傳的圖片，並限制使用者上傳圖片的時間間隔需大於3秒
async def get_upload_image(img_id: str):
    url=f"https://api-data.line.me/v2/bot/message/{img_id}/content"

    # post跟get都要寫下面那一行程式碼
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            stream = response.content
            st = await stream.read()
            img = Image.open(io.BytesIO(st))
#             # img.show()
#     # print("return image")
    # print(type(img))
    return img

# 辨識圖片成功的回覆訊息(帶入用戶名跟植物名)
async def identify_success(species: str,userid: str) -> dict:
    user_name = await get_user_name(userid)
    plant_name_with_spaces = f" {trans_dict[species]} "
    msg = {
        "type": "text",
        "text": trans_dict["idsuc"].replace("[人名]", user_name).replace("[植物名]", plant_name_with_spaces)
    }
    return msg

# 辨識圖片失敗的回覆訊息
async def identify_fail() -> dict:
    msg = {
        "type": "text",
        "text": trans_dict["idfail"]
    }
    return msg

# quick reply:是否再次辨識植物
async def retry_confirm() -> dict:
    return await quick_reply(trans_dict["idagain"], [{"action_type": "postback", "label": trans_dict["y"], "data": "idplant"}, \
                            {"action_type": "postback", "label": trans_dict["n"], "data": trans_dict["thxuse"]}])

# 使用者不再辨識植物時回覆的感謝使用訊息
async def thx_use_msg() -> dict:
    msg = {
        "type": "text",
        "text": trans_dict["thxuse"]
    }
    return msg

# quick reply
async def quick_reply(text: str, actions: list) -> dict:
    quick_reply_items = []

    for action in actions:
        item = {
            "type": "action",
            "imageUrl": action.get("imageUrl"),
            "action": {
                "type": action["action_type"],
                "label": action["label"]
                # add additional field for each message type 對每種訊息類別增加額外的字段
            }
        }
        # check there is icon or not 確認quick reply選項是否有附加icon
        try:
            item["imageUrl"] = action["imageUrl"]
        except:
            pass
        # Add additional parameters based on action type 依照action的型別新增額外的參數
        if action["action_type"] == "postback":
            item["action"]["data"] = action.get("data")
        elif action["action_type"] == "uri":
            item["action"]["uri"] = action.get("uri")

        quick_reply_items.append(item)

    msg = {
        "type": "text",
        "text": text,
        "quickReply": {
            "items": quick_reply_items
        }
    }

    return msg

# 外來種植物辨識功能-上傳一張植物圖片，附有上傳圖片及開啟相機的功能
async def upload_image() -> dict:
    imageUrl_a = "https://storage.googleapis.com/green01/identify/1.png"
    imageUrl_b = "https://storage.googleapis.com/green01/identify/2.png"
    
    return await quick_reply(trans_dict["upaimg"], \
                             [{"imageUrl":imageUrl_a, "action_type":"cameraRoll", "label":trans_dict["upimg"]},\
                              {"imageUrl":imageUrl_b, "action_type":"camera", "label":trans_dict["cameraon"]}])

# 旋轉木馬選單-歷史紀錄查詢功能(列出使用者辨識成功的植物種類)
async def get_history(user_records: list, data: dict) -> dict:

    msg = {
            "type": "template",
            "altText": "歷史紀錄查詢(列出使用者辨識成功的植物種類)",
            "template": {
                "type": "carousel",
                "columns": []
            }
    }
    # carousel 10 records -> quick reply -> carousel other records
    # unique_record: 學名, image_url
    for record in user_records:
        plant = get_plants(record["_id"])
        name = plant["scientific name"]
        data = {"species": name,"action": "showup", "skip": 0}

        column ={
            "thumbnailImageUrl": plant["imgurl"],
            "imageBackgroundColor": "#FFFFFF",
            "title": trans_dict[name],
            "text": name,
            "actions": [
                {
                    "type": "postback",
                    "label": trans_dict["vimgin"], #查看更多資訊
                    "data": json.dumps(data)
                },
            ]
        }
        msg["template"]["columns"].append(column)
    return msg
        

# 圖片旋轉木馬選單-歷史紀錄查詢功能(列出使用者辨識成功的植物圖片資訊)
async def display_history(records: dict) -> dict:

    msg = {
            "type": "template",
            "altText": "歷史紀錄查詢(列出使用者辨識成功的植物圖片資訊)",
            "template": {
                "type": "image_carousel",
                "columns":[],
            }
        }
            # carousel 5 records -> quick reply -> carousel next 5 records
        
            # unique_record: 學名, image_url
    for record in records: 
        record = record["records"]          
        column = {
            "imageUrl": record["imgurl"],
            "action": {
                "type": "postback",
                "label": trans_dict["dl"],
                "data": record["imgurl"]
            } 
        }
        msg["template"]["columns"].append(column)
        
    return msg

# 歷史紀錄查詢點選圖片旋轉木馬選單後出現使用者拍攝的圖片(供分享、下載)
async def share_img(data: str) -> dict:

    msg = {
        "type": "image",
        "originalContentUrl": data,
        "previewImageUrl": data
    }
    return msg
# 取得使用者名稱
async def get_user_name(userid: str) -> str:
    # 從redis暫存中取出使用者名稱 
    user_name = r.hget(name=userid, key="display_name")

    if user_name:
        return user_name
    
    url = f"https://api.line.me/v2/bot/profile/{userid}"
    headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            res = await response.json()
            # print(res)
            user_name = res["displayName"]
            # 使用者名稱暫存到redis
            r.hset(name=userid, key="display_name", value=user_name)

        return user_name

# 是否再查看先前的歷史紀錄quick reply 按否的回覆: 好好欣賞植物圖片吧!   
async def view_image_info() -> dict:
    msg = {
            "type": "text",
            "text": trans_dict["enjimg"]
        }
    return msg

# 是否再顯示其他的植物種類quick reply 按否的回覆:點選上方的「查看更多資訊」吧!
async def click_view_info() -> dict:
    msg = {
        "type": "text",
        "text": trans_dict["clvimgin"]
    }
    return msg   

# 取得圖文選單id
async def get_richmenu_id():
    url = "https://api.line.me/v2/bot/richmenu/{richMenuId}"
    headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}"}
    req = requests.get(url=url,headers=headers)

# 傳送網頁端登入資訊
async def login_info(userid: str, display_name: str)  -> str:

    # 使用者名稱如果有空格的話要移除
    display_name = display_name.replace(" ", "")

    mode = await language(userid)
    token = await get_access_token(userid, display_name)

    uri = web_dns + f"?source=True&userid={userid[:7]}&mode={mode}&token={token}"
    # print(uri)

    return uri

# 取得網頁access token
async def get_access_token(userid: str, display_name: str) -> str: # 修改display_name中的空格
    csrf_token = await get_csrf_token()

    # 使用者名稱如果有空格的話要移除
    display_name = display_name.replace(" ", "")
    
    data = {
        "userid" : userid[:7],
        "display_name" : display_name
    }
    # print("test", csrf_token)
    headers = {"X-CSRFToken":csrf_token}
    cookies = {"csrftoken" : csrf_token} 
    async with aiohttp.ClientSession() as session:
        async with session.post(url=access_token_url, data=data, cookies=cookies, headers=headers) as resp:
            # print(resp)
            data = await resp.json()
            token = data["token"]
            return token

# Forbidden (CSRF cookie not set.): /users/line_login
# Forbidden (CSRF token missing.): /users/line_login

# 取得網頁csrf token
async def get_csrf_token() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(csrf_url) as resp:
            data = await resp.json()
            csrf_token = data["csrf_token"]
            return csrf_token
        

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port= 8000)