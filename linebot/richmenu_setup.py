import requests
import configparser

# 帶入config.ini檔案裏面的資訊
config = configparser.ConfigParser()
config.read("config.ini")

headers= {
    "Content-type": "application/json",
    "Authorization": F"Bearer {config.get('line-bot', 'channel_access_token')}"
}

trans_dict = {"idplant":["外來種植物辨識","Identify Invasive Plants","外来種植物を識別する"]}

#中文選單
body = {
    "size": {"width": 2500, "height": 1686},    # 設定尺寸
    "selected": "true",                         # 預設是否顯示
    "name": "chinese",                          # 選單名稱
    "chatBarText": "開啟圖文選單",                  # 選單在 LINE 顯示的標題
    "areas":[                                   # 選單內容
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 200},# 中文按鈕座標及大小
            "action": {"type": "postback", "data": "no-data"} # 中文按鈕使用postback
        },
        {
            "bounds": {"x": 834, "y": 0, "width":833, "height": 200}, # English按鈕座標及大小
            "action": {"type": "richmenuswitch", "richMenuAliasId": "english",
                    "data": "richmenu-changed-to-english"} # 轉換到英文圖文選單
        },
        {
            "bounds": {"x": 1667, "y": 0, "width":833, "height": 200}, # 日本語按鈕座標及大小
            "action": {"type": "richmenuswitch", "richMenuAliasId": "japanese",
                    "data": "richmenu-changed-to-japanese"} # 轉換到日文圖文選單
        },
        {
            "bounds": {"x": 0, "y": 201, "width":833, "height": 740}, # 常見問題按鈕座標及大小
            "action": {"type": "uri", "uri": "https://taiwan.wwg.solutions/plants/FAQ" }
        },
        {
            "bounds": {"x": 834, "y": 201, "width":833, "height": 740}, # 開發人員按鈕座標及大小
            "action":{"type": "uri", "uri": "https://taiwan.wwg.solutions/plants/developers"}
        },
        {
            "bounds": {"x": 1667, "y": 201, "width":833, "height": 740}, # 網頁按鈕座標及大小
            "action":{"type": "postback", "data": "weblog"} 
        },
        {
            "bounds": {"x": 0, "y": 941, "width":1250, "height": 740}, # 外來種植物辨識按鈕座標及大小
            "action":{"type": "postback", "data": "idplant"}
        },
        {
            "bounds": {"x": 1251, "y": 941, "width":1250, "height": 740}, # 歷史紀錄查詢按鈕座標及大小
            "action": {"type": "postback", "data": "{'action': 'search', 'skip': 0}"} 
        }
    ]
}


#上傳得到richmenuid A(中文)
url = "https://api.line.me/v2/bot/richmenu"
req = requests.post(url=url,json=body,headers=headers) 
data = req.json()
richmenuA_id = data["richMenuId"]
print("中文: ", richmenuA_id)

#圖片下載 chinese.jpg
with open("./img/chinese.png", "rb") as f:
    image_data = f.read()

#上傳圖文資料(中文圖片)/content
url = f"https://api-data.line.me/v2/bot/richmenu/{richmenuA_id}/content"
headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"image/png"}
req = requests.post(url=url, headers=headers, data=image_data)
print(req.status_code)

#將中文圖文選單 id 和別名 Alias id 綁定
url="https://api.line.me/v2/bot/richmenu/alias"
headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"application/json"}
body = {
    "richMenuAliasId":"chinese",
    "richMenuId":richmenuA_id
}
req = requests.post(url=url,headers=headers, json=body)
print(req.status_code)

#英文選單
body = {
    "size": {"width": 2500, "height": 1686},    # 設定尺寸
    "selected": "true",                        # 預設是否顯示
    "name": "english",                     # 選單名稱
    "chatBarText": "open richmenu",              # 選單在 LINE 顯示的標題
    "areas":[                                  # 選單內容
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 200},# 中文按鈕座標及大小
            "action": {"type": "richmenuswitch", "richMenuAliasId": "chinese",
                    "data": "richmenu-changed-to-chinese"} # 轉換到中文圖文選單
        },
        {
            "bounds": {"x": 834, "y": 0, "width":833, "height": 200}, # English按鈕座標及大小
            "action": {"type": "postback", "data": "no-data"} # 英文按鈕使用postback 
        },
        {
            "bounds": {"x": 1667, "y": 0, "width":833, "height": 200}, # 日本語按鈕座標及大小
            "action": {"type": "richmenuswitch", "richMenuAliasId": "japanese",
                    "data": "richmenu-changed-to-japanese"} # 轉換到日文圖文選單
        },
        {
            "bounds": {"x": 0, "y": 201, "width":833, "height": 740}, # 常見問題按鈕座標及大小
            "action": {"type": "uri", "uri": "https://taiwan.wwg.solutions/plants/lan_mode?mode=en&next=/plants/FAQ"} 
        },
        {
            "bounds": {"x": 834, "y": 201, "width":833, "height": 740}, # 開發人員按鈕座標及大小
            "action":{"type": "uri", "uri": "https://taiwan.wwg.solutions/plants/lan_mode?mode=en&next=/plants/developers"} 
        },
        {
            "bounds": {"x": 1667, "y": 201, "width":833, "height": 740}, # 網頁按鈕座標及大小
            "action":{"type": "postback", "data": "weblog"} 
        },
        {
            "bounds": {"x": 0, "y": 941, "width":1250, "height": 740}, # 外來種植物辨識按鈕座標及大小
            "action":{"type": "postback", "data": "idplant"}
        },
        {
            "bounds": {"x": 1251, "y": 941, "width":1250, "height": 740}, # 歷史紀錄查詢按鈕座標及大小
            "action": {"type": "postback", "data": "{'action': 'search', 'skip': 0}"} 
        }
    ]
}


#上傳得到richmenuid B(英文)
url = "https://api.line.me/v2/bot/richmenu"
req = requests.post(url=url ,json=body,headers=headers)
data = req.json() 
richmenuB_id = data["richMenuId"]
print("英文: ",richmenuB_id)

#圖片下載 english.jpg
with open("./img/english.png", "rb") as f:
    image_data = f.read()

#上傳圖文資料(英文圖片)/content
url = f"https://api-data.line.me/v2/bot/richmenu/{richmenuB_id}/content"
headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"image/png"}
req = requests.post(url=url, headers=headers, data=image_data)
print(req.status_code)

#將英文圖文選單 id 和別名 Alias id 綁定
url="https://api.line.me/v2/bot/richmenu/alias"
headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"application/json"}
body = {
    "richMenuAliasId":"english",
    "richMenuId":richmenuB_id
}
req = requests.post(url=url,headers=headers, json=body)
print(req.status_code)

#日文選單
body = {
    "size": {"width": 2500, "height": 1686},    # 設定尺寸
    "selected": "true",                        # 預設是否顯示
    "name": "japanese",                     # 選單名稱
    "chatBarText": "リッチメニューを開く",              # 選單在 LINE 顯示的標題
    "areas":[                                  # 選單內容
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 200},# 中文按鈕座標及大小
            "action": {"type": "richmenuswitch", "richMenuAliasId": "chinese", # 轉換到中文圖文選單
                    "data": "richmenu-changed-to-chinese"}
        },
        {
            "bounds": {"x": 834, "y": 0, "width":833, "height": 200}, # English按鈕座標及大小
            "action": {"type": "richmenuswitch", "richMenuAliasId": "english",
                    "data": "richmenu-changed-to-english"} # 轉換到英文圖文選單
        },
        {
            "bounds": {"x": 1667, "y": 0, "width":833, "height": 200}, # 日本語按鈕座標及大小
            "action": {"type": "postback", "data": "no-data"} # 日文按鈕使用postback
        },
        {
            "bounds": {"x": 0, "y": 201, "width":833, "height": 740}, # 常見問題按鈕座標及大小
            "action": {"type": "uri", "uri": "https://taiwan.wwg.solutions/plants/lan_mode?mode=jp&next=/plants/FAQ"}
        },
        {
            "bounds": {"x": 834, "y": 201, "width":833, "height": 740}, # 開發人員按鈕座標及大小
            "action":{"type": "uri", "uri": "https://taiwan.wwg.solutions/plants//lan_mode?mode=jp&next=/plants/developers"} 
        },
        {
            "bounds": {"x": 1667, "y": 201, "width":833, "height": 740}, # 網頁按鈕座標及大小
            "action":{"type": "postback", "data": "weblog"}
        },
        {
            "bounds": {"x": 0, "y": 941, "width":1250, "height": 740}, # 外來種植物辨識按鈕座標及大小
            "action":{"type": "postback", "data": "idplant"}
        },
        {
            "bounds": {"x": 1251, "y": 941, "width":1250, "height": 740}, # 歷史紀錄查詢按鈕座標及大小
            "action": {"type": "postback", "data": "{'action': 'search', 'skip': 0}"} 
        }
    ]
}


#上傳得到richmenuid C(日文)
url = "https://api.line.me/v2/bot/richmenu"
req = requests.post(url=url ,json=body,headers=headers) 
data = req.json()
richmenuC_id = data["richMenuId"]
print("日文: ",richmenuC_id)

#圖片下載 japanese.jpg
with open("./img/japanese.png", "rb") as f:
    image_data = f.read()

#上傳圖文資料(日文圖片)/content
url = f"https://api-data.line.me/v2/bot/richmenu/{richmenuC_id}/content"
headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"image/png"}
req = requests.post(url=url, headers=headers, data=image_data)
print(req.status_code)

#將日文圖文選單 id 和別名 Alias id 綁定
url="https://api.line.me/v2/bot/richmenu/alias"
headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"application/json"}
body = {
    "richMenuAliasId":"japanese",
    "richMenuId":richmenuC_id
}
req = requests.post(url=url,headers=headers, json=body )
print(req.status_code)

#通知
urls = [
    f"https://api.line.me/v2/bot/user/all/richmenu/{richmenuC_id}",
    f"https://api.line.me/v2/bot/user/all/richmenu/{richmenuB_id}",
    f"https://api.line.me/v2/bot/user/all/richmenu/{richmenuA_id}"]

headers = {"Authorization":f"Bearer {config.get('line-bot', 'channel_access_token')}","Content-Type":"application/json"}

for url in urls:
    req = requests.post(url=url, headers=headers)
    print(req.status_code)
