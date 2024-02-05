from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import CustomUserModel
from urllib import parse
import requests
import json
from django.conf import settings
from django.contrib.auth import authenticate, login
# Create your views here.


# doing line login and get/create the user then login web
def line_login(request):

    if request.method == 'GET':
        # get userid and display name
        # if userid alreadly in model, change display name
        # else get_or_create user
        auth_code = request.GET.get("code", None)
        state = request.GET.get("state", None)

        if auth_code and state:
            # post request to line platform
            HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = "https://api.line.me/oauth2/v2.1/token"
            FormData = {"grant_type": 'authorization_code', "code": auth_code, "redirect_uri": f"{settings.LINE_LOGIN_ENDPOINT}/users/line_login", \
                        "client_id": settings.LINE_LOGIN_ID, "client_secret":settings.LINE_LOGIN_SECRET}
            data = parse.urlencode(FormData)
            content = requests.post(url=url, headers=HEADERS, data=data).text
            content = json.loads(content)
            # get user profile
            url = "https://api.line.me/v2/profile"
            HEADERS = {'Authorization': content["token_type"]+" "+content["access_token"]}
            content = requests.get(url=url, headers=HEADERS).text
            content = json.loads(content)

            # get userid and nme to create user
            name = content["displayName"]
            userID = content["userId"]

            # create user or update existing user name
            if CustomUserModel.objects.filter(userid=userID).exists():
                # update display 
                obj, created = CustomUserModel.objects.update_or_create(userid=userID, display_name=name)
                pass
            else:
                obj, created = CustomUserModel.objects.get_or_create(userid=userID, display_name=name)
            
            # authenticate the user and sign in
            user = authenticate(request, userid=userID, display_name=name)

            if user:
                login(request, user)

            # get language mode from cookie
            code = request.session.get("lan_mode", "chi")
            # get next 
            next = request.GET.get("next", default= "/plants/")
            # add parameters to lan_redirect url to redirect back to sub page.
            url = f"/plants/lan_mode?code={code}&next={next}"

            return redirect(url)
        else:
            settings.TRANS_DICT["end_point"] = settings.LINE_LOGIN_ENDPOINT
            settings.TRANS_DICT["id"] = settings.LINE_LOGIN_ID
            return render(request, "users/line_login.html", settings.TRANS_DICT)
        
# route for line richmenu to auto-login directly
def auto_login(request):
    if request.method == "GET":
        request.GET.get()