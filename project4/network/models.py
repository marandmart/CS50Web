from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="user")
    post = models.TextField(max_length=240, null=False, blank=False)
    time = models.DateField(null=False, blank=False)
    likes = models.ManyToManyField(User, related_name="liked", blank=True)
    dislikes = models.ManyToManyField(User, related_name="disliked", blank=True)

    def __str__(self):
        return f"{self.user} posted {self.post}"

class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name="user_followed")
    followers = models.ManyToManyField(User, blank=True, related_name="follows")
    following = models.ManyToManyField(User, blank=True, related_name="followed")
    
    def __str__(self):
        return f"{self.user}: followed by {self.followers} and follows {self.following}"