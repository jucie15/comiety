from django.contrib.gis.db import models
from dongzip.models import School
import re




class SchoolLocation(models.Model):
    school = models.OneToOneField(School)
    point = models.PointField(srid = 4326) # 학교 위치 좌표
    #point = 'POINT(x y)'로 디비 저장

    def __str__(self):
        return self.school.name

    def lng(self):
        lng_point= float(str(self.point)[17:27])
        return lng_point

    def lat(self):
        lat_point= float(str(self.point)[28:37])
        return lat_point