from django.db import models
from django.utils import timezone

class Info(models.Model):
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    peoplenum = models.TextField(max_length=10, null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    mbti = models.CharField(max_length=10, null=True, blank=True)
    army = models.CharField(max_length=10, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    body = models.CharField(max_length=10, null=True, blank=True)
    eyes = models.CharField(max_length=10, null=True, blank=True)
    face = models.CharField(max_length=10, null=True, blank=True)
    hobby = models.CharField(max_length=100, null=True, blank=True)
    jobs = models.CharField(max_length=100, blank=True, null=True)
    avgage = models.IntegerField(null=True, blank=True)
    ages = models.TextField(null=True, blank=True)  # 정수로 이루어진 리스트를 문자열로 저장
    kakao_id = models.CharField(max_length=100, blank=True, null=True)  # kakao_id를 기본 키로 설정
    free = models.TextField(null=True, blank=True)
    kakaotalk_id = models.CharField(max_length=20, null=True, blank=True)
    you_kakao_id = models.CharField(max_length=100, blank=True, null=True)
    matching_time = models.DateTimeField(null=True, blank=True)

    # 매칭 성사 여부 (IntegerField로 변경)
    matching_success = models.IntegerField(default=0)

    # 매칭 신청 여부
    matching_application = models.IntegerField(default=0)

    # 매칭 동의 여부
    matching_agreement = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)