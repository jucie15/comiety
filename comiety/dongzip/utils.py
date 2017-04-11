import os
from dongzip.models import *
from geodjango.models import *
from django.conf import settings


ROOT = lambda *args: os.path.join(settings.BASE_DIR, 'dongzip', *args)

def school_db_create():
    with open(ROOT("addr.txt"),"rt") as f:
        addr = f.read()
    addr_list = addr.split("|")

    with open(ROOT("name.txt"),"rt") as f:
        name = f.read()
    name_list = name.split("|")

    with open(ROOT("latlng.txt"),"rt") as f:
        latlng = f.read()
    latlng_list = latlng.split("|")

    for name, addr, latlng in zip(name_list,addr_list,latlng_list):

        lat = latlng.split(',')[0]
        lng = latlng.split(',')[1]
        sch = School()

        sch.name = name
        sch.address = addr
        sch.save()

        sch_loc = SchoolLocation()
        print("sch_loc1")
        sch_loc.school = sch
        print("sch_loc2")

        sch_loc.point = 'POINT(' + lng +' ' + lat + ')'
        print(sch_loc.point)

        sch_loc.save()

#school_db_create()
