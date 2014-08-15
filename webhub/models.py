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


#Post table stores details about posts

class Post(models.Model):
    #The owner of the post
    owner = models.ForeignKey(Pcuser, null=False, related_name='owner')
    #title
    title_post = models.CharField(max_length=300)
    #description
    description_post = models.CharField(max_length=2000)
    #link to important documents
    link_post = models.CharField(max_length=2000)
    #field to note the timestamp when the post was created
    created = models.DateTimeField(auto_now_add=True)
    #field to note the timestamp when the post was last updated
    updated = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return self.owner.user.username
    
#Post table stores details about revision history of edit of the posts

class RevPost(models.Model):
    #The post which is being edited
    owner_rev_post = models.ForeignKey(Post, null=False, related_name='owner_rev_post')
    #The user who is editing the post
    owner_rev = models.ForeignKey(Pcuser, null=False, related_name='owner_rev')
    #revised title
    title_post_rev = models.CharField(max_length=300)
    #revised description
    description_post_rev = models.CharField(max_length=2000)
    
    
    
    #field to note the timestamp when the revised version was created
    created = models.DateTimeField(auto_now_add=True)
    #change in title
    title_change = models.BooleanField(default=False)
    #change in description
    description_change = models.BooleanField(default=False)
    
  
    

    def __unicode__(self):
        return self.owner_rev.user.username    

    
#Peacetrack begins here

class Region(models.Model):
    #Name of the region
    region_name = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.region_name    
        
class Sector(models.Model):
    #Name of the sector
    sector_name = models.CharField(max_length=300)
    #Description of the sector
    sector_desc = models.CharField(max_length=3000)
    #Code of the sector
    sector_code = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.sector_name    
    

class PTPost(models.Model):
    #Name of the post
    post_name = models.CharField(max_length=300)
    #The region with which the post is associated
    post_region = models.ForeignKey(Region, null=False, related_name='post_region')
    #many to many relationship with the Sector
    sector = models.ManyToManyField(Sector)
    
    def __unicode__(self):
        return self.post_name    
    
class Project(models.Model):
    #Name of the project
    project_name = models.CharField(max_length=300)
    #Purpose of the project
    project_purpose = models.CharField(max_length=3000)
    #The sector with which the project is associated
    project_sector = models.OneToOneField(Sector, primary_key=True)

    def __unicode__(self):
        return self.project_name    
    
class Goal(models.Model):
    #Name of the goal
    goal_name = models.CharField(max_length=300)
    #Title of the goal
    goal_title = models.CharField(max_length=1000)
    #Statement of the goal
    goal_stmt = models.CharField(max_length=3000)
    #The project with which the goal is associated
    goal_project = models.ForeignKey(Region, null=False, related_name='goal_project')
    
    def __unicode__(self):
        return self.goal_name    
    
class Objective(models.Model):
    #Name of the objective
    obj_name = models.CharField(max_length=300)
    #Title of the objective
    obj_title = models.CharField(max_length=1000)
    #Statement of the objective
    obj_stmt = models.CharField(max_length=3000)
    #The goal with which the objective is associated
    obj_goal = models.ForeignKey(Goal, null=False, related_name='obj_goal')
    
    def __unicode__(self):
        return self.obj_name    
    
class Indicator(models.Model):
    #The objective with which the indicator is associated
    ind_obj = models.ForeignKey(Objective, null=False, related_name='ind_obj')
    #Indicator description
    #Indicator type (SI/PDI/SO/PD)
    #0 - SI
    #1 - PDI
    #2 - SO
    #3 - PD
    ind_type_1 = models.CharField(max_length="100", default="None", null=False)
    #Indicator type (Outcome/Output)
    #true - Outcome
    #false - Output
    ind_type_2 = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.ind_type_1

    
    
class Output(models.Model):
    #The sector with which the output is associated
    output_sector = models.ForeignKey(Sector, null=False, related_name='output_sector')
    #The country(post) with which the output is associated
    output_ptpost= models.ForeignKey(PTPost, null=False, related_name='output_ptpost')
    #The indicator with which the output is associated
    output_ind= models.ForeignKey(Indicator, null=False, related_name='output_ind')
    #integer (the output)
    output_value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.output_value)

    
class Outcome(models.Model):
    #The sector with which the outcome is associated
    outcome_sector = models.ForeignKey(Sector, null=False, related_name='outcome_sector')
    #The country(post) with which the outcome is associated
    outcome_ptpost= models.ForeignKey(PTPost, null=False, related_name='outcome_ptpost')
    #The indicator with which the outcome is associated
    outcome_ind= models.ForeignKey(Indicator, null=False, related_name='outcome_ind')
    #integer (the outcome)
    outcome_value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.outcome_value)
    
    
class Cohort(models.Model):
    #name
    cohort_name = models.CharField(max_length=300)
    #short description
    cohort_desc = models.CharField(max_length=3000)
    #no of members
    cohort_no_of_members = models.IntegerField()
    #age range
    cohort_age = models.CharField(max_length=30)
    #no of males
    cohort_males = models.IntegerField()
    #no of females
    cohort_females = models.IntegerField()
    #position within the community
    cohort_pos = models.CharField(max_length=30)
    #other relevant notes
    cohort_notes = models.CharField(max_length=3000)
    
    def __unicode__(self):
        return unicode(self.cohort_name)
    
class Activity(models.Model):
    #title of the activity
    activity_title = models.CharField(max_length=300)
    #short description
    activity_desc = models.CharField(max_length=3000)
    #relevant cohort name
    activity_cohort = models.ForeignKey(Cohort, null=False, related_name='activity_cohort')
    #date & time of the activity creation
    activity_created = models.DateTimeField(auto_now_add=True)
    #output with which the activity is associated
    activity_output = models.ForeignKey(Output, null=False, related_name='activity_output')
    
    def __unicode__(self):
        return self.activity_title
    
class Measurement(models.Model):
    #title of the Measurement
    meas_title = models.CharField(max_length=300)
    #short description of the Measurement
    meas_desc = models.CharField(max_length=3000)
    #relevant cohort name
    meas_cohort = models.ForeignKey(Output, null=False, related_name='meas_cohort')
    #date & time of the Measurement creation
    meas_created = models.DateTimeField(auto_now_add=True)
    #outcome with which the Measurement is associated
    meas_outcome = models.ForeignKey(Outcome, null=False, related_name='meas_outcome')
    
    def __unicode__(self):
        return self.meas_title
    

    
class Volunteer(models.Model):
    #username
    vol_name = models.CharField(max_length=300)
    #email
    vol_email = models.CharField(max_length=300)
    #sector
    vol_sector = models.ForeignKey(Sector, null=False, related_name='vol_sector')
    #country
    vol_ptpost = models.ForeignKey(PTPost, null=False, related_name='vol_ptpost')
    #activity
    vol_activity = models.ManyToManyField(Activity)
    #measurement
    vol_meas = models.ManyToManyField(Measurement)
    #cohort
    vol_cohort = models.ManyToManyField(Cohort)
    
    def __unicode__(self):
        return self.vol_name

