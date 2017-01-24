from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.


class School(models.Model):
    name = models.CharField(max_length = 128, blank = False, null = False) # 학교 이름
    address = models.CharField(max_length = 256, blank = False, null = False) # 학교 주소
    member_number = models.IntegerField(default = 0, blank = False, null = False) # 멤버 수
    society_number = models.IntegerField(default = 0 , blank = False, null = False) # 동아리 수
    description = models.TextField(max_length = 512, blank = True, null = True) # 학교 소개

    def __str__(self):
        return self.name

class Profile(models.Model):
    # user = models.OneToOneField(User)
    # user = models.OneToOneField('auth.User')
    school = models.ForeignKey(School) # School Table과 1:n 관계 형성
    user = models.OneToOneField(settings.AUTH_USER_MODEL)  # 'auth.User'
    nickname = models.CharField(max_length = 128, blank = False, null = False) # 닉네임
    #favorite = 태그로 ㄱ?
    tel_number = models.CharField(max_length = 32, blank = False, null = False) # 전화번호

    def __str__(self):
        return self.user.username

class Society(models.Model):
    school = models.ForeignKey(School) # School Table과 1:n 관계 형성
    name = models.CharField(max_length = 128, blank = False, null = False) # 동아리 이름
    main_tel_number = models.CharField(max_length = 32, blank = False, null = False) # 대표 전화번호
    member_number = models.IntegerField(default = 0, blank = False, null = False) # 멤버 수
    address = models.CharField(max_length = 256, blank = False, null = False) # 동아리 주소
    description = models.TextField(max_length = 512, blank = True, null = True) # 동아리 소개
    users = models.ManyToManyField(Profile) # USER TABLE과 다대다 관계 형성
    #category  = models.CharField # 관심사 및 카테고리를 따로 빼야하나?

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length = 128, blank = False, null = False) # 행사 명
    event_date = models.DateTimeField() # 행사 일정
    created_at = models.DateTimeField(auto_now_add = True) # 행사 일정 등록 시간
    updated_at = models.DateTimeField(auto_now_add = True) # 행사 일정 수정 시간
    description = models.TextField(max_length = 512, blank = True, null = True) # 행사 소개

    home_team = models.ForeignKey(Society, related_name='home_event_set') # 주최 팀
    # for event in society.home_event_set.all()으로 접근 가능

    # away_team_set = models.ManyToManyField(Society) # 어웨이 팀이 여려 팀일 경우
    away_team = models.ForeignKey(Society, related_name='away_event_set') # 상대 팀
    # society.away_event_set.all()으로 접근 가능

    def __str__(self):
        return self.title
