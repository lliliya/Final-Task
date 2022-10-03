from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce import HTMLField


class User(AbstractBaseUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    email_verify = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=100, editable=True)
    REQUIRED_FIELDS = ['username']


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=100)
    text = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.header}-{self.user}'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    reply_text = models.TextField()
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='replies')


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
