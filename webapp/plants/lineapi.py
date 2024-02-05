from django.conf import settings
import aiohttp
# {'events': [{'source': {'type': 'user', 'userId': '{userid}'}, 'data': '{data}', 'img_name': '{img_name}'}]} 當作data值去輸入
headers = {'Content-Type': 'application/json'}


async def get_user_data(userid):
    payload = {'events': [{'source': {'type': 'user', 'userId': userid }}]}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=settings.LINE_API_URL, headers=headers, json=payload) as res:
            print(res.status)
            user_data = await res.json()
            return user_data


async def save_user_data(userid, data, species):
    payload = {'events': [{'source': {'type': 'user', 'userId': f'{userid}'}, 
                           'data': data, 
                           'species': species }]}
    async with aiohttp.ClientSession() as session:
        res = await session.post(url=settings.LINE_API_URL, data=payload)
        print(res.status)
        return res.status