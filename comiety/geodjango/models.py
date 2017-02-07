from django.contrib.gis.db import models
from dongzip.models import School

class SchoolLocation(models.Model):
    school = models.OneToOneField(School)
    point = models.PointField(srid = 4326) # admin에서 지도 사용 없앨 수 있으면 없애거나 x,y필드 사용
