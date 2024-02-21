from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUserModel
from urllib import parse
import requests
import json
import secrets
import hashlib
import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token

# Create your views here.


# def line_login(request):
#     # print(request.GET)
    
#     if request.method == "GET":

#         return render(request, "users/line_login.html", settings.TRANS_DICT)
    
#     elif request.method == "POST":
#         print(request.body)
#         userid = request.POST.get("userid")
#         display_name = request.POST.get("display_name")

#         # check where the POST request from
#         source = request.POST.get("source", "web")

#         # get signup for line
#         signup = request.POST.get("signup", False)

#         # if POST from linebot, update display name if needed
#         if signup:
#             obj, created = CustomUserModel.objects.update_or_create(userid=userid, defaults={"display_name":display_name})
#         print(userid, display_name, signup)
#         # authenticate user info then login
#         user = authenticate(request, userid=userid, display_name=display_name)

#         if user:
#             print("Good")
#             login(request, user)

#             if source == "line":
#                 code = request.POST.get("mode")
#             else:
#                 # get language mode from session
#                 code = request.session.get("lan_mode", "chi")
            
#             # get next 
#             # print(request.GET)
#             next = request.POST.get("next", default= "/plants/")

#             # add parameters to lan_redirect url to redirect back to sub page.
#             url = f"/plants/lan_mode?code={code}&next={next}"
#             return redirect(url)         
                
#         else:
#             print("here")
#             settings.TRANS_DICT["error"] = True 
#             return render(request, "users/line_login.html", settings.TRANS_DICT)


def line_login(request):
    # print(request.GET)
    
    if request.method == "GET":

        source = request.GET.get("source", False)

        # handle the line autologin
        if source:
            # get info
            userid = request.GET.get("userid")
            encoded = request.GET.get("token")
            mode = request.GET.get("mode")
            print(encoded, type(encoded))

            key = CustomUserModel.objects.get(userid=userid).password

            decoded = jwt.decode(encoded, key, algorithms="HS256")

            # extract userid and display_name
            userid, display_name = list(decoded.items())[0]

            user = authenticate(request, userid=userid, display_name=display_name)

            if user:
                print("Good")
                login(request, user)
                print(request.user.is_authenticated)

                url = f"/plants/lan_mode?mode={mode}&next=/plants/"

                return redirect(url)
            
            else:
                print("here")
                settings.TRANS_DICT["error"] = True 
                return render(request, "users/line_login.html", settings.TRANS_DICT)


        return render(request, "users/line_login.html", settings.TRANS_DICT)
    
    # for web login
    elif request.method == "POST":
        print(request.body)
        userid = request.POST.get("userid")
        display_name = request.POST.get("display_name")

        # authenticate user info then login
        user = authenticate(request, userid=userid, display_name=display_name)

        if user:
            print("Good")
            login(request, user)

            # get language mode from session
            mode = request.session.get("lan_mode", "chi")
            
            # get next 
            next = request.POST.get("next", default= "/plants/")

            # add parameters to lan_redirect url to redirect back to sub page.
            url = f"/plants/lan_mode?mode={mode}&next={next}"
            return redirect(url)         
                
        else:
            print("here")
            settings.TRANS_DICT["error"] = True 
            return render(request, "users/line_login.html", settings.TRANS_DICT)

def get_access_token(request):

    if request.method == "POST":

        # extract userid and name
        userid = request.POST.get("userid")
        display_name = request.POST.get("display_name")
        key = secrets.token_urlsafe(32)

        obj, created = CustomUserModel.objects.update_or_create(userid=userid, defaults={"display_name":display_name, "password":key})

        # generate key for jwt and save into session
        # hash_user = hashlib.sha256(userid.encode("utf-8")).hexdigest()

        # print("access", userid.encode("utf-8"), hash_user)

        # encode by jwt
        encoded = jwt.encode({userid:display_name}, key, algorithm="HS256")
        print(encoded)
        return JsonResponse({"token": encoded})

def csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})


def line_logout(request):
    logout(request)
    return redirect("plants:index")
    
# doing line login and get/create the user then login web
# def line_login(request):

#     if request.method == 'GET':
#         # get userid and display name
#         # if userid alreadly in model, change display name
#         # else get_or_create user
#         auth_code = request.GET.get("code", None)
#         state = request.GET.get("state", None)

#         if auth_code and state:
#             # post request to line platform
#             HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
#             url = "https://api.line.me/oauth2/v2.1/token"
#             FormData = {"grant_type": 'authorization_code', "code": auth_code, "redirect_uri": settings.LINE_LOGIN_ENDPOINT, \
#                         "client_id": settings.LINE_LOGIN_ID, "client_secret":settings.LINE_LOGIN_SECRET}
#             data = parse.urlencode(FormData)
#             content = requests.post(url=url, headers=HEADERS, data=data).text
#             content = json.loads(content)
#             # get user profile
#             url = "https://api.line.me/v2/profile"
#             HEADERS = {'Authorization': content["token_type"]+" "+content["access_token"]}
#             content = requests.get(url=url, headers=HEADERS).text
#             content = json.loads(content)

#             # get userid and nme to create user
#             name = content["displayName"]
#             userID = content["userId"]

#             # create user or update existing user name
#             if CustomUserModel.objects.filter(userid=userID).exists():
#                 # update display 
#                 obj, created = CustomUserModel.objects.update_or_create(userid=userID, display_name=name)
#                 pass
#             else:
#                 obj, created = CustomUserModel.objects.get_or_create(userid=userID, display_name=name)
            
#             # authenticate the user and sign in
#             user = authenticate(request, userid=userID, display_name=name)

#             if user:
#                 login(request, user)

#             # get language mode from cookie
#             code = request.session.get("lan_mode", "chi")
#             # get next 
#             next = request.GET.get("next", default= "/plants/")
#             # add parameters to lan_redirect url to redirect back to sub page.
#             url = f"/plants/lan_mode?code={code}&next={next}"

#             return redirect(url)
#         else:
#             settings.TRANS_DICT["endpoint"] = settings.LINE_LOGIN_ENDPOINT
#             settings.TRANS_DICT["id"] = settings.LINE_LOGIN_ID
#             return render(request, "users/line_login.html", settings.TRANS_DICT)
        
# route for line richmenu to auto-login directly
# def auto_login(request):
#     if request.method == "GET":
#         userid = request.GET.get("userid")
#         try:
#             obj = get_object_or_404(CustomUserModel, userid=userid)

#             user = authenticate(request, userid=obj.userid, display_name=obj.display_name)

#             if user:
#                 login(request, user)

#             return redirect("plants:index")
#         except CustomUserModel.DoesNotExist:
#             raise Http404("No existing user")
        