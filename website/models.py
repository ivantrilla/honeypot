from django.db import models

# Create your models here.
class BadActor(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
