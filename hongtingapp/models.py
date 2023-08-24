from django.db import models


class UserProfile(models.Model):
    age = models.CharField(max_length=2, default='')
    gender = models.CharField(max_length=1, default='')
    #group_size = models.CharField(max_length=1, default='')
    major = models.CharField(max_length=100, default='')
    mbti = models.CharField(max_length=4, default='')  # MBTI 유형
    army = models.CharField(max_length=10, default='')  # 군/미필
    height = models.CharField(max_length=20, default='')  # 키
    body = models.CharField(max_length=20, default='')  # 체형, 얼굴상
    eyes = models.CharField(max_length=20, default='')  # 유/무쌍
    hobby = models.CharField(max_length=100, default='')  # 관심사
    self_intro = models.TextField()  # 자유로운 자기소개

    #def __str__(self):
    #    return f"{self.age}세 {self.get_gender_display()} {self.get_group_size_display()}"

    class Meta:
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필"


class Info(models.Model):
    peoplenums = models.CharField(max_length=10)
    jobs = models.CharField(max_length=10)
    locations = models.CharField(max_length=10)
    ages = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)