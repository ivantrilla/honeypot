from django.shortcuts import render
from django.contrib import messages 
from .models import BadActor

def home_view(request):
    return render(request, "website/home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password")
        ip_address = request.META.get("REMOTE_ADDR")

        if username.lower() == "admin" or username.lower() == "anonymous":
            messages.success(request, "Entry accepted")
        else:
            messages.error(request, "Error: Unauthorized user")

        user = BadActor(username=username, password=password, ip_address=ip_address)
        user.save()
        
    return render(request, "website/login.html")