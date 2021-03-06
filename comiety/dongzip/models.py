import re
from django.conf import settings
from django.db import models
# from django.contrib.gis.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.forms import ValidationError

# validator 전화번호
def tel_number_validator(value):
    if not re.match(r'^01\d{9}$', value):
        raise ValidationError("""전화번호('-'없이, 11자)를 정확히 입력해 주세요""")

class School(models.Model):
    name = models.CharField(max_length = 128, blank = False, null = False) # 학교 이름
    address = models.CharField(max_length = 256, blank = False, null = False) # 학교 주소
    member_number = models.IntegerField(default = 0, blank = False, null = False) # 멤버 수
    society_number = models.IntegerField(default = 0 , blank = False, null = False) # 동아리 수
    description = models.TextField(max_length = 512, blank = True, null = True) # 학교 소개

    def __str__(self):
        return self.name

    def update_member_number(self):
        # school instance를 통해 reverse match(profile_set)하고 저장한다.(member_number 필드만 업데이트)
        self.member_number = self.profile_set.all().count()
        self.save(update_fields=['member_number'])

    def update_society_number(self):
        self.society_number = self.society_set.all().count()
        self.save(update_fields=['society_number'])


class Profile(models.Model):
    # user = models.OneToOneField(User)
    # user = models.OneToOneField('auth.User')
    school = models.ForeignKey(School) # School Table과 1:n 관계 형성
    user = models.OneToOneField(settings.AUTH_USER_MODEL)  # 'auth.User' 인증 라이브러리를 사용하기 위해 auth.user 사용
    nickname = models.CharField(max_length = 128, blank = False, null = False) # 닉네임
    tel_number = models.CharField(max_length = 32, blank = False, null = False, validators=[tel_number_validator]) # 전화번호
    favorite_society = models.ManyToManyField('Society') # 관심 동아리
    profile_image = models.ImageField(upload_to = 'uploaded/user_profile/', null = True, blank = True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def on_post_save(sender, **kwargs):
        # profile에 의해 post_save가 호출 됐을 경우 실행
        profile = kwargs['instance']
        if kwargs['created']:
            profile.school.update_member_number()

#post_save = sender가save함수를 호출 했을 떄 함수(Profile.on_post_save)를 호출 한다. <-> prefix.save()
post_save.connect(Profile.on_post_save, sender = Profile)

class Society(models.Model):
    school = models.ForeignKey(School) # School Table과 1:n 관계 형성
    name = models.CharField(max_length = 128, blank = False, null = False) # 동아리 이름
    main_tel_number = models.CharField(max_length = 32, blank = False, null = False) # 대표 전화번호
    description = models.TextField(max_length = 512, blank = True, null = True) # 동아리 소개
    users = models.ManyToManyField(Profile, through = 'Membership') # USER TABLE과 다대다 관계 형성
    categorys = models.ManyToManyField('Category', blank = True)
    logo_image = models.ImageField(upload_to = 'uploaded/society_profile/', null = True, blank = True)
    background_image = models.ImageField(upload_to = 'uploaded/society_profile/', null = True, blank = True)

    def __str__(self):
        return self.name

    @staticmethod
    def on_post_save(sender, **kwargs):
        # profile에 의해 post_save가 호출 됐을 경우 실행
        society = kwargs['instance']
        if kwargs['created']:
            society.school.update_society_number()

post_save.connect(Society.on_post_save, sender = Society)

class Membership(models.Model):
    user = models.ForeignKey(Profile)
    society = models.ForeignKey(Society)
    power = models.IntegerField(default = 0)
    joined_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '{}.{}'.format(self.user, self.society)


class Event(models.Model):
    title = models.CharField(max_length = 128, blank = False, null = False) # 행사 명
    event_date = models.DateTimeField() # 행사 일정
    created_at = models.DateTimeField(auto_now_add = True) # 행사 일정 등록 시간
    updated_at = models.DateTimeField(auto_now = True) # 행사 일정 수정 시간
    description = models.TextField(max_length = 512, blank = True, null = True) # 행사 소개

    home_team = models.ForeignKey(Society, related_name='home_event_set') # 주최 팀
    # for event in society.home_event_set.all()으로 접근 가능

    # away_team_set = models.ManyToManyField(Society) # 어웨이 팀이 여려 팀일 경우
    away_team = models.ForeignKey(Society, related_name='away_event_set') # 상대 팀
    # society.away_event_set.all()으로 접근 가능

    def __str__(self):
        return self.title

class Category(models.Model):
    url_name = models.CharField(max_length = 32)
    name = models.CharField(max_length = 32)

    def __str__(self):
        return self.url_name
