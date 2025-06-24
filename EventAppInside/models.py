# Create your models here.
from django.db import models

class Photo_store(models.Model):
    photo = models.BinaryField()
    photo_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=100)
    event_type = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.photo_name} ({self.location})"

    

class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    image_data = models.BinaryField()  # stores image as binary

    def __str__(self):
        return self.photo_name


class Registration(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user_name


class AdminUser(models.Model):
    admin_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Again, hash recommended

    def __str__(self):
        return self.admin_name
    


class Like(models.Model):
    photo = models.ForeignKey(Photo_store, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)  # Assume basic user auth for now
    liked = models.BooleanField(default=False)

class Comment(models.Model):
    photo = models.ForeignKey(Photo_store, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

