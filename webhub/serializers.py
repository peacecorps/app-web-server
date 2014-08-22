from django.contrib.auth.models import User
from webhub.models import *

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email','id')


class PcuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pcuser
        fields = ('user', 'location', 'phone', 'gender','id')
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('owner', 'title_post', 'description_post', 'created','updated','id')
        
        
class RevPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevPost
        fields = ('owner_rev_post', 'owner_rev', 'title_post_rev', 'description_post_rev', 'created','id','title_change','description_change','id')
        
#Peacetrack begins here

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('region_name','id')
        
        
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ('sector_name','sector_desc','sector_code','id')

class PTPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTPost
        fields = ('post_name','post_region','sector','id')
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_name','project_purpose','project_sector')
        
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('goal_name','goal_title','goal_stmt','goal_project','id')
        
class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ('obj_name','obj_title','obj_stmt','obj_goal','id')
        
class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ('ind_obj','ind_type_1','ind_type_2','id')
        
class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ('output_sector','output_ptpost','output_ind','output_value','id')
        

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ('outcome_sector','outcome_ptpost','outcome_ind','outcome_value','id')
        
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('activity_title','activity_desc','activity_cohort','activity_created','activity_output','id')
    
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('meas_title','meas_desc','meas_cohort','meas_created','meas_outcome','id')

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('cohort_name','cohort_desc','cohort_no_of_members','cohort_age','cohort_males','cohort_females','cohort_pos','cohort_notes','id')
        
class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ('vol_name','vol_sector','vol_ptpost','vol_activity','vol_meas','vol_cohort','id')