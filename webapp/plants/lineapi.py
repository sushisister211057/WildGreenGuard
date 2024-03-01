from django.conf import settings
import aiohttp
import logging
import json

# reference format from line: {'events': [{'source': {'type': 'user', 'userId': '{userid}'}, 'data': '{data}', 'img_name': '{img_name}'}]} 

# get user data from mongodb throuh line
async def get_user_data(userid):
    """
    get user data from mongodb throuh line

    params:

    userid: str

    return user data 
    """
    
    headers = {'Content-Type': 'application/json'}
    payload = {'events': [{'source': {'type': 'user', 'userId': userid }}]}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=settings.LINE_API_URL, headers=headers, json=payload) as res:
            logging.info(f"get user request: {res.status}")
            user_data = await res.json()
            return user_data

# send data to mongodb through line
async def save_user_data(userid:str, data:bytes, species, isinvasive):
    """
    send data to mongodb through line

    params:

    userid: str
    data: image data in bytes you want to save
    species: str, name of species you want to save
    isinvasive: bool

    """

    payload = {"events": [{"source": {"type": "user", "userId": userid}, "species": species, "isinvasive":isinvasive}]}
    
    formdata = aiohttp.FormData()
    formdata.add_field("payload", json.dumps(payload), content_type="application/json")
    formdata.add_field("image", data, content_type="image/jpeg")
    

    async with aiohttp.ClientSession() as session:
        async with session.post(url=settings.LINE_API_URL, data=formdata) as res:
            logging.info(f"save user request: {res.status}")
            return res.status