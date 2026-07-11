from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
