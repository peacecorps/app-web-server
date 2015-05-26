#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com


from django.contrib import admin
from webhub.models import *


admin.site.register(Pcuser)
admin.site.register(Post)
admin.site.register(RevPost)
admin.site.register(Region)
admin.site.register(Sector)
admin.site.register(PTPost)
admin.site.register(Project)
admin.site.register(Goal)
admin.site.register(Objective)
admin.site.register(Indicator)
admin.site.register(Output)
admin.site.register(Outcome)
admin.site.register(Activity)
admin.site.register(Measurement)
admin.site.register(Cohort)
admin.site.register(Volunteer)



# Register your models here.
