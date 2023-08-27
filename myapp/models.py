from django.db import models

class Info(models.Model):
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    peoplenum = models.CharField(max_length=10, null=True, blank=True)
    job = models.CharField(max_length=10, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    mbti = models.CharField(max_length=4, null=True, blank=True)
    army = models.CharField(max_length=10, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    body = models.CharField(max_length=10, null=True, blank=True)
    eyes = models.CharField(max_length=10, null=True, blank=True)
    face = models.CharField(max_length=10, null=True, blank=True)
    hobby = models.CharField(max_length=20, null=True, blank=True)
    jobs = models.CharField(max_length=10, blank=True, null=True)
    locations = models.CharField(max_length=100, blank=True, null=True)
    ages = models.IntegerField(blank=True, null=True)
    kakao_id = models.CharField(max_length=100, primary_key=True)  # kakao_id를 기본 키로 설정

    def __str__(self):
        return str(self.pk)
