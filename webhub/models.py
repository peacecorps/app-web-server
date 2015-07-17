from django.db import models
from django.contrib.auth.models import User

import os

# To update the filename of the newly uploaded photo
def update_filename(instance, filename):
    path = '/vagrant/submit/media/propics/'
    format = instance.user.username + ".jpg"
    return os.path.join(path, format)



# Django provides a table called user that stores basic user information like username, password and email id.
class Pcuser(models.Model):
    #username
    user = models.OneToOneField(User)
    #location
    location = models.CharField(max_length=300)
    #phone number
    phone = models.CharField(max_length=150)
    #gender
    gender = models.CharField(max_length=10)
    #for reset_password
    reset_pass = models.CharField(default="",max_length=320)
    
    
    #path to default user image
    image = models.CharField(max_length=300, default="http://i.imgur.com/dnjclWV.png")
    #image
    imageobj = models.ImageField(upload_to=update_filename)
    
    #verification status
    #1 - unverified
    #any other number = verification code
    verified = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.user.username
