#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
import os
from uuid import uuid4

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
    
    def __unicode__(self):
        return self.user.username
    
    
#Post table stores details about posts

class Post(models.Model):
    #The owner of the post
    owner = models.ForeignKey(Pcuser, null=False, related_name='owner')
    #title
    title_post = models.CharField(max_length=300)
    #description
    description_post = models.CharField(max_length=2000)
    
    def __unicode__(self):
        return self.owner.user.username