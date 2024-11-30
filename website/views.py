from django.shortcuts import render
from django.contrib import messages 
from .models import BadActor,UrlPath,CountryName,Credential
import json
import requests
from django.db.models import Count

def home_view(request):
    countrynames = [f"{country.name}" for country in CountryName.objects.all()]
    countrydata = [country.times_used for country in CountryName.objects.all()] 
   
    pathnames = [f"{path.name}" for path in UrlPath.objects.all()]
    pathdata = [path.times_used for path in UrlPath.objects.all()]

    queryset = Credential.objects.values('username').annotate(count=Count('username'))
    username = [f"Username: {item['username']}" for item in queryset]
    usernamedata = [item['count'] for item in queryset]  


    queryset = Credential.objects.values('password').annotate(count=Count('password'))
    passwordnamelabels = [f"Password: {item['password']}" for item in queryset]  
    passworddata = [item['count'] for item in queryset] 


    context = {
        'countrynames': countrynames,
        'countrydata': countrydata,
        'pathnames' : pathnames,
        'pathdata': pathdata,
        'usernamelabels': username,
        'usernamedata': usernamedata,
        'passwordnamelabels' : passwordnamelabels,
        'passworddata' : passworddata
    }
    return render(request, "website/home.html",context=context)

def bait_login_view(request):
    if request.method == "POST":
        post_username = request.POST.get("username") 
        post_password = request.POST.get("password")
        post_ip_address = request.META.get("REMOTE_ADDR")
        post_ip_address = "0.0.0.0"

        try:
            post_credential = Credential.objects.get(username=post_username,password=post_password)
        except:
            post_credential = Credential(username=post_username,password=post_password)
            post_credential.save()
        
        post_credential.times_used = int(post_credential.times_used) +1
        post_credential.save()


        try: post_path = UrlPath.objects.get(name=request.path)
        except: 
            post_path = UrlPath(name=request.path)
            post_path.save()

        post_path.times_used = int(post_path.times_used) + 1
        post_path.save()


        if post_ip_address != "127.0.0.1": post_country = "Spain" 
        post_country = "EU"
        
        
        try: post_country = CountryName.objects.get(name=post_country)
        except: 
            post_country = CountryName(name=post_country)
            post_country.save()

        post_country.times_used = int(post_country.times_used) +1
        post_country.save()

        
        try: 
            BadActorObject = BadActor.objects.get(ip_address=post_ip_address)
        except:
            print("El badactor no existe")
            BadActorObject = BadActor(ip_address=post_ip_address,country=post_country)
            BadActorObject.save()

        BadActorObject.credenial.add(post_credential)
        BadActorObject.url_path.add(post_path)
    

        messages.error(request, "Error: Unauthorized user")
    
    return render(request, "website/login.html")
