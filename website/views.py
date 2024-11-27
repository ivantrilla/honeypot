from django.shortcuts import render
from django.contrib import messages 
from .models import User

def home_view(request):
    return render(request, "website/home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        ip_address = request.META.get("REMOTE_ADDR")

        if username.lower() == "admin" or username.lower() == "anonymous":
            messages.success(request, "Entry accepted")
        else:
            messages.error(request, "Error: Unauthorized user")

        user = User(username=username, ip_address=ip_address)
        user.save()
        
    return render(request, "website/login.html")