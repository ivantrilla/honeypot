from django.contrib import admin
from .models import BadActor,UrlPath,CountryName,Credential

admin.site.register(BadActor)
admin.site.register(UrlPath)
admin.site.register(CountryName)
admin.site.register(Credential)
