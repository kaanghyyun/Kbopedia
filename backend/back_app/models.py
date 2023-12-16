from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils import timezone
from django.conf import settings
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    author = models.CharField(max_length=200)

    def __str__(self):
        """A string representations of the model."""    
        return self.title


    def increase_count(self):
        self.count += 1
        self.save()


class CustomUser(AbstractUser):
    kakao_user_id = models.CharField(max_length=255, unique=True)
    kakao_access_token = models.CharField(max_length=255, blank=True, null=True)    # 로그인 토큰
    kakao_nickname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.kakao_nickname

    @classmethod
    def create_kakao_user(cls, username, kakao_nickname, kakao_access_token):
        user = cls(username=username, kakao_access_token=kakao_access_token, kakao_nickname=kakao_nickname)
        user.set_password(kakao_access_token)
        user.save()

        return user