import secrets
import logging
import jwt
from django.http import  JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUserModel
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token

# Create your views here.

# for user line login
def line_login(request):
    
    if request.method == "GET":

        source = request.GET.get("source", False)

        # handle the line autologin
        if source:
            # get info
            userid = request.GET.get("userid")
            encoded = request.GET.get("token")
            mode = request.GET.get("mode")
            logging.debug(f"{encoded}, {type(encoded)}")

            key = CustomUserModel.objects.get(userid=userid).password

            decoded = jwt.decode(encoded, key, algorithms="HS256")

            # extract userid and display_name
            userid, display_name = list(decoded.items())[0]

            user = authenticate(request, userid=userid, display_name=display_name)

            if user:
                login(request, user)
                logging.debug(f"user login: {request.user.is_authenticated}")

                url = f"/plants/lan_mode?mode={mode}&next=/plants/"

                return redirect(url)
            
            else:
                settings.TRANS_DICT["error"] = True 
                return render(request, "users/line_login.html", settings.TRANS_DICT)

        return render(request, "users/line_login.html", settings.TRANS_DICT)
    
    # for web login
    elif request.method == "POST":
        userid = request.POST.get("userid")
        display_name = request.POST.get("display_name")

        # authenticate user info then login
        user = authenticate(request, userid=userid, display_name=display_name)

        if user:
            login(request, user)
            logging.debug(f"user login: {request.user.is_authenticated}")

            # get language mode from session
            mode = request.session.get("lan_mode", "chi")
            
            # get next 
            next = request.POST.get("next", default= "/plants/")

            # add parameters to lan_redirect url to redirect back to sub page.
            url = f"/plants/lan_mode?mode={mode}&next={next}"
            return redirect(url)         
                
        else:
            settings.TRANS_DICT["error"] = True 
            return render(request, "users/line_login.html", settings.TRANS_DICT)

# set token for user login authentication
def get_access_token(request):

    if request.method == "POST":

        # extract userid and name
        userid = request.POST.get("userid")
        display_name = request.POST.get("display_name")
        key = secrets.token_urlsafe(32)

        # update or create user from userid and display_name
        obj, created = CustomUserModel.objects.update_or_create(userid=userid, defaults={"display_name":display_name, "password":key})

        # encode by jwt
        encoded = jwt.encode({userid:display_name}, key, algorithm="HS256")

        return JsonResponse({"token": encoded})

# for user to get csrf
def csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})

# for user logout
def line_logout(request):
    logout(request)
    return redirect("plants:index")
