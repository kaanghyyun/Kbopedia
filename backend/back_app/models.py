from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        """A string representations of the model."""    
        return self.title

    def increase_count(self):
        self.count += 1
        self.save()


class User(models.Model):
    email = models.TextField()
    password = models.TextField()
    name = models.TextField()
    nickname = models.TextField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    def to_dto(self):
        pass

    def __str__(self):
        return f"[{self.name}/{self.nickname}] -> {self.email}"

class CustomUser(AbstractUser):
    kakaonickname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return str(self.nickname)