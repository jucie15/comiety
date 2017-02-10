from django.contrib.gis.db import models
from dongzip.models import School

class SchoolLocation(models.Model):
    school = models.OneToOneField(School)
    point = models.PointField(srid = 4326) # 학교 위치 좌표
    #point = 'POINT(x y)'로 디비 저장
