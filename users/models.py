from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    LOGIN_FACEBOOK = "facebook"
    LOGIN_GITHUB = "github"
    LOGIN_GOOGLE = "google"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"

    LOGIN_CHOICES = (
        (LOGIN_FACEBOOK, "Facebook"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_NAVER, "Naver"),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=50, default="", blank=True)
    login_method = models.CharField(choices=LOGIN_CHOICES, max_length=10)
