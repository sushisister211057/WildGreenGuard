import requests
import configparser

# 帶入config.ini檔案裏面的資訊
config = configparser.ConfigParser()
config.read("config.ini")

#查詢別名
url="https://api.line.me/v2/bot/richmenu/alias/list"
headers= {
    # 'Content-type': 'application/json',
    "Authorization": F"Bearer {config.get('line-bot', 'channel_access_token')}"
}
req = requests.get(url=url, headers=headers)
data = req.json()

# 找出RichMenuAliasId
richMenuAliasIds = []
for alias in data["aliases"]:
    richMenuAliasIds.append(alias["richMenuAliasId"])

print(richMenuAliasIds)

# 刪除RichMenuAliasId
for richMenuAliasId in richMenuAliasIds :
    url= f"https://api.line.me/v2/bot/richmenu/alias/{richMenuAliasId}" #不可動
    req = requests.delete(url=url, headers=headers)
    print(req.status_code)

#查詢richmenuId
url="https://api.line.me/v2/bot/richmenu/list"
req = requests.get(url=url, headers=headers)
data = req.json()

richMenuIds = []
for richMenuId in data["richmenus"]:
    richMenuIds.append(richMenuId["richMenuId"])

print(richMenuIds)

# 刪除richmenuid
for richMenuId in richMenuIds:
    url= f"https://api.line.me/v2/bot/richmenu/{richMenuId}" #不可動
    req = requests.delete(url=url, headers=headers)
    print(req.status_code)

