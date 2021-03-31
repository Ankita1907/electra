from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


class Question(models.Model):
    q_no = models.IntegerField(default=0)
    question_text = models.CharField(max_length=1000)
    answd = models.BooleanField(default=False)
    image = models.ImageField(upload_to="electra/images", default="img1.jpg")

    def __str__(self):
        return self.question_text

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.question)


class Point(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    ans = models.ForeignKey(Response, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    comment = models.TextField()
    points = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    image = models.TextField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRW6X2lldt_gy2tcbXCKBbKWNVBpH-f1Mcjsw&usqp=CAU")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
        print('profile creatd')



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile_for_new_user, sender=settings.AUTH_USER_MODEL)

