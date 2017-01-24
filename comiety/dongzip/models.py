from django.db import models
from django.utils import timezone
# Create your models here.



class User(models.Model):
    name = models.CharField(max_length = 128, blank = False, null = False) # 유저 이름
    nickname = models.CharField(max_length = 128, blank = False, null = False) # 닉네임
    #favorite = 태그로 ㄱ?
    tel_number = models.CharField(max_length = 32, blank = False, null = False) # 전화번호
    email = models.EmailField(max_length = 128, blank = False, null = False) # 이메일

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length = 128, blank = False, null = False) # 학교 이름
    address = models.CharField(max_length = 256, blank = False, null = False) # 학교 주소
    member_number = models.IntegerField(default = 0, blank = False, null = False) # 멤버 수
    society_number = models.IntegerField(default = 0 , blank = False, null = False) # 동아리 수
    description = models.TextField(max_length = 512, blank = True, null = True) # 학교 소개

    def __str__(self):
        return self.name

class Society(models.Model):
    name = models.CharField(max_length = 128, blank = False, null = False) # 동아리 이름
    main_tel_number = models.CharField(max_length = 32, blank = False, null = False) # 대표 전화번호
    member_number = models.IntegerField(default = 0, blank = False, null = False) # 멤버 수
    address = models.CharField(max_length = 256, blank = False, null = False) # 동아리 주소
    description = models.TextField(max_length = 512, blank = True, null = True) # 동아리 소개
    #category  = models.CharField # 관심사 및 카테고리를 따로 빼야하나?

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length = 128, blank = False, null = False) # 행사 명
    event_date = models.DateTimeField() # 행사 일정
    created_at = models.DateTimeField(auto_now_add = True) # 행사 일정 등록 시간
    updated_at = models.DateTimeField(auto_now_add = True) # 행사 일정 수정 시간
    description = models.TextField(max_length = 512, blank = True, null = True) # 행사 소개

    # home_team = models.ForeignKey(Society)
    # away_team = models.ForeignKey(Society)

    def __str__(self):
        return self.title
