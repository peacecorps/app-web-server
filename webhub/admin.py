#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com


from django.contrib import admin
from webhub.models import Pcuser
from webhub.models import Post

admin.site.register(Pcuser)
admin.site.register(Post)

# Register your models here.
