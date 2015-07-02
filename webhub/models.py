#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import os
from uuid import uuid4
from paths import cpspath

    
#To update the filename of the newly uploaded photo
def update_filename(instance, filename):
    path = '/vagrant/submit/media/propics/'
    format = instance.user.username + ".jpg"
    return os.path.join(path, format)



#Django provides a table called user that stores basic user information like username, password and email id.
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

# Post table stores details about posts


class Post(models.Model):
    # The owner of the post
    owner = models.ForeignKey(Pcuser, null=False, related_name='owner')
    title_post = models.CharField(max_length=100,
                                  validators=[
                                      RegexValidator(
                                          r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)|(:)]+$'
                                      )]
                                  )
    description_post = models.CharField(max_length=5000,
                                        validators=[
                                            RegexValidator(
                                                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)|(:)]+$'
                                            )]
                                        )
    # link to important documents
    link_post = models.CharField(max_length=2000)
    # field to note the timestamp when the post was created
    created = models.DateTimeField(auto_now_add=True)
    # field to note the timestamp when the post was last updated
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.owner.user.username

# Post table stores details about revision history of edit of the posts


class RevPost(models.Model):
    # The post which is being edited
    owner_rev_post = models.ForeignKey(Post,
                                       null=False,
                                       related_name='owner_rev_post')
    # The user who is editing the post
    owner_rev = models.ForeignKey(Pcuser, null=False, related_name='owner_rev')
    # revised title
    title_post_rev = models.CharField(max_length=300)
    # revised description
    description_post_rev = models.CharField(max_length=2000)
    # field to note the timestamp when the revised version was created
    created = models.DateTimeField(auto_now_add=True)
    # change in title
    title_change = models.BooleanField(default=False)
    # change in description
    description_change = models.BooleanField(default=False)

    def __unicode__(self):
        return self.owner_rev.user.username
