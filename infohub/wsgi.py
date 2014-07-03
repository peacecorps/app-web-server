#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infohub.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
