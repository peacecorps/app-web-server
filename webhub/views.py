#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import jinja2
import uuid
from jinja2.ext import loopcontrols
from webhub.checker import check
from webhub.models import *
from rest_framework import viewsets
from webhub.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from paths import cpspath

import smtplib

#SMTP port for sending emails
SMTP_PORT = 465

#link for the localhost
website = "http://192.168.33.10:8000"

jinja_environ = jinja2.Environment(loader=jinja2.FileSystemLoader(['ui']), extensions=[loopcontrols])

#apis for malaria begin here
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
#List all pcusers, or create a new pcuser.
@api_view(['GET', 'POST'])
def pcuser_list(request):
    if request.method == 'GET':
        pcuser = Pcuser.objects.all()
        serializer = PcuserSerializer(pcuser, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PcuserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a pcuser instance.
@api_view(['GET', 'PUT', 'DELETE'])
def pcuser_detail(request, pk):
    try:
        pcuser = Pcuser.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PcuserSerializer(pcuser)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PcuserSerializer(pcuser, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pcuser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
        
    
    
    
#List all posts, or create a new post.
@api_view(['GET', 'POST'])
def post_list(request):
     if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = PostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a post instance.
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class RevPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RevPost.objects.all()
    serializer_class = RevPostSerializer        

#List all revision of a posts
@api_view(['GET', 'POST'])
def revpost_list(request):
     if request.method == 'GET':
        revpost = RevPost.objects.all()
        serializer = RevPostSerializer(revpost, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = RevPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a revpost instance.
@api_view(['GET', 'PUT', 'DELETE'])
def revpost_detail(request, pk):
    try:
        revpost = RevPost.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RevPostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RevPostSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        revpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
#apis for malaria end here

#apis for peacetrack begin here

#for regions
class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer        

#List all region
@api_view(['GET', 'POST'])
def region_list(request):
     if request.method == 'GET':
        region = Region.objects.all()
        serializer = RegionSerializer(region, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = RegionSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a region instance.
@api_view(['GET', 'PUT', 'DELETE'])
def region_detail(request, pk):
    try:
        region = Region.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegionSerializer(region)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RegionSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for sectors
class SectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer        

#List all sectors
@api_view(['GET', 'POST'])
def sector_list(request):
     if request.method == 'GET':
        sector = Sector.objects.all()
        serializer = SectorSerializer(sector, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = SectorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a sector instance.
@api_view(['GET', 'PUT', 'DELETE'])
def sector_detail(request, pk):
    try:
        sector = Sector.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectorSerializer(sector)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SectorSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sector.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

#for ptposts
class PTPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PTPost.objects.all()
    serializer_class = PTPostSerializer        

#List all ptpost
@api_view(['GET', 'POST'])
def ptpost_list(request):
     if request.method == 'GET':
        ptpost = PTPost.objects.all()
        serializer = PTPostSerializer(ptpost, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = PTPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a ptpost instance.
@api_view(['GET', 'PUT', 'DELETE'])
def ptpost_detail(request, pk):
    try:
        ptpost = PTPost.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PTPostSerializer(ptpost)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PTPostSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ptpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#error    
#for projects
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer        

#List all projects
@api_view(['GET', 'POST'])
def project_list(request):
     if request.method == 'GET':
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a project instance.
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

    
#for goals
class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer        

#List all goal
@api_view(['GET', 'POST'])
def goal_list(request):
     if request.method == 'GET':
        goal = Goal.objects.all()
        serializer = GoalSerializer(goal, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = GoalSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a goal instance.
@api_view(['GET', 'PUT', 'DELETE'])
def goal_detail(request, pk):
    try:
        goal = Goal.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GoalSerializer(goal)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GoalSerializer(goal, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
        
#for objectives
class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer        

#List all objective
@api_view(['GET', 'POST'])
def objective_list(request):
     if request.method == 'GET':
        objective = Objective.objects.all()
        serializer = ObjectiveSerializer(objective, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = ObjectiveSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a objective instance.
@api_view(['GET', 'PUT', 'DELETE'])
def objective_detail(request, pk):
    try:
        objective = Objective.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ObjectiveSerializer(objective)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ObjectiveSerializer(objective, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objective.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
#for indicators
class IndicatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer        

#List all indicator
@api_view(['GET', 'POST'])
def indicator_list(request):
     if request.method == 'GET':
        indicator = Indicator.objects.all()
        serializer = IndicatorSerializer(indicator, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = IndicatorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a indicator instance.
@api_view(['GET', 'PUT', 'DELETE'])
def indicator_detail(request, pk):
    try:
        indicator = Indicator.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IndicatorSerializer(indicator)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IndicatorSerializer(indicator, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        indicator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for outputs
class OutputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Output.objects.all()
    serializer_class = OutputSerializer        

#List all output
@api_view(['GET', 'POST'])
def output_list(request):
     if request.method == 'GET':
        output = Output.objects.all()
        serializer = OutputSerializer(output, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = OutputSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a output instance.
@api_view(['GET', 'PUT', 'DELETE'])
def output_detail(request, pk):
    try:
        output = Output.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OutputSerializer(output)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OutputSerializer(output, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        output.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    
#for outcomes
class OutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer        

#List all outcome
@api_view(['GET', 'POST'])
def outcome_list(request):
     if request.method == 'GET':
        outcome = Outcome.objects.all()
        serializer = OutcomeSerializer(outcome, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = OutcomeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a outcome instance.
@api_view(['GET', 'PUT', 'DELETE'])
def outcome_detail(request, pk):
    try:
        outcome = Outcome.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OutcomeSerializer(outcome)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OutcomeSerializer(outcome, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        outcome.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for activitys
class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer        

#List all activity
@api_view(['GET', 'POST'])
def activity_list(request):
     if request.method == 'GET':
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a activity instance.
@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, pk):
    try:
        activity = Activity.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivitySerializer(activity, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
#for measurements
class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer        

#List all measurement
@api_view(['GET', 'POST'])
def measurement_list(request):
     if request.method == 'GET':
        measurement = Measurement.objects.all()
        serializer = MeasurementSerializer(measurement, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = MeasurementSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a measurement instance.
@api_view(['GET', 'PUT', 'DELETE'])
def measurement_detail(request, pk):
    try:
        measurement = Measurement.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeasurementSerializer(measurement)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeasurementSerializer(measurement, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        measurement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for cohurts
class CohurtViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Cohurt.objects.all()
    serializer_class = CohurtSerializer        

#List all cohurt
@api_view(['GET', 'POST'])
def cohurt_list(request):
     if request.method == 'GET':
        cohurt = Cohurt.objects.all()
        serializer = CohurtSerializer(cohurt, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = CohurtSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a cohurt instance.
@api_view(['GET', 'PUT', 'DELETE'])
def cohurt_detail(request, pk):
    try:
        cohurt = Cohurt.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CohurtSerializer(cohurt)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CohurtSerializer(cohurt, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cohurt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for volunteers
class VolunteerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer        

#List all volunteer
@api_view(['GET', 'POST'])
def volunteer_list(request):
     if request.method == 'GET':
        volunteer = Volunteer.objects.all()
        serializer = VolunteerSerializer(volunteer, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = VolunteerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a volunteer instance.
@api_view(['GET', 'PUT', 'DELETE'])
def volunteer_detail(request, pk):
    try:
        volunteer = Volunteer.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VolunteerSerializer(volunteer, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        volunteer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

#apis for peacetrack end here

        
        
        
        
        
        
        

    
#Calls index page
def index(request):
    return HttpResponse(jinja_environ.get_template('index.html').render({"pcuser":None}))
    
#Calls dashboard wish is shown after a user is logged in
def dashboard(request):
    
    retval = check(request)
    if retval <> None:
        return retval
    
    template_values = {'pcuser' : request.user.pcuser,
                    }
    return HttpResponse(jinja_environ.get_template('dashboard.html').render(template_values)) 


#Calls the signup page. If the user us already logged in, s/he will be redirected to dashboard.
def signup_page(request):
    if request.user.is_authenticated():
        redirect_url = "/"
        if 'redirect_url' in request.REQUEST.keys():
            redirect_url = request.REQUEST['redirect_url']
        return HttpResponse(jinja_environ.get_template('redirect.html').render({"pcuser":None,"redirect_url":redirect_url}))

    else:
        return HttpResponse(jinja_environ.get_template('signup.html').render({"pcuser":None}))
    
    
#Called when a user clicks submit button in signup. Here a verification mail is also sent to the user.
@csrf_exempt
def signup_do(request):
    if request.user.is_authenticated():
        logout(request)
        redirect_url = "/"
        if 'redirect_url' in request.REQUEST.keys():
            redirect_url = request.REQUEST['redirect_url']
        return HttpResponse(jinja_environ.get_template('redirect.html').render({"pcuser":None,"redirect_url":redirect_url}))
    
    username = request.REQUEST['username']
    password = request.REQUEST['password']
    confirmpassword = request.REQUEST['confirmpassword']
        
    if password <> confirmpassword:
      return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                            "text":'<p>Passwords don\'t match. Please Enter again.</p><p>Click OK to go back to signup page.</p>',"link":'/signup_page/'}))
    
    first_name = request.REQUEST['first_name']
    last_name = request.REQUEST['last_name']
    phone = request.REQUEST['phone']
    email = request.REQUEST['email']
    gender = request.REQUEST['gender']
    location = request.REQUEST['location']

    try:
        if len(User.objects.filter(email=email))<>0:
            return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                                  "text":'<p>Someone has already registered using this email.</p><p>If you have forgotten your password, click <a href=\'/forgot_pass/\'</p><p>Click <a href=\'/signup_page/\'>here</a> to go back to signup page.</p>',"link":'0'}))
    except:
        pass
    
    if '@' not in email or '.' not in email:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'<p>Invalid email, please Enter again.</p><p>Go Back or click OK to go to signup page.</p>',"link":"/signup_page/"}))
    
        
    if first_name == "":
        first_name = username
    
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    entry = Pcuser(user=user, phone=phone, gender=gender, location=location, verified = uuid.uuid4().hex)
        
    entry.save()
    #send email to user
    login_do(request)
    send_verification_email(request)
    
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'<p>Verification email sent. check your inbox and verify the account.</p>',"text1":'<p>Go Back or click OK to go to signup page.</p>',"link":'/signup_page/'}))
    

    
#Function to send verification mail to user's email after he signs up.
def send_verification_email(request):
    if not request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('index.html').render({"pcuser":None}))

    try:
        request.user.pcuser
    except:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'No Pcuser associated!. Please go back or click  to go to the homepage' , "link": '/'}))
    entry=request.user
    subject = 'Peace Corps Verification Email'
    msg = 'Subject: %s \n\nYour email has been registered on pchub.com.\nPlease\
    click on the following link to verify (or copy paste it in your browser if needed)\n\n\
    %s/verify?code=%s\n\nIf you have not registered on our website, please ignore.' % (subject, website, entry.pcuser.verified)
    
    x = send_email(msg, entry.email)
    if x[0]==0:
        return x[1]
    
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser, "text":'<p>Verification Email sent! Please Check your email inbox.</p><p>To re-send verification email, click <a href=\'/send_verification_email/\'>here</a>.</p><p>Click <a href=\'/logout_do/\'>here</a> to go to the homepage and log-in again</p>', "link":'0'}))



#Function to send emails using google smtplib. Takes email id and message as input.    
def send_email(msg, email):
    gmailLogin = 'ranipc93'
    gmailPas = 'ranipc1993'
    fro = gmailLogin + "@gmail.com"
    
    to = email
    
    server = smtplib.SMTP_SSL('smtp.googlemail.com',SMTP_PORT)
    a = server.login( gmailLogin, gmailPas)
    server.sendmail(fro, to,msg)
    return (1,1)


#Called when a user enters verification code and clicks on submit. Checks the verification code with database.
def verify(request):
    if not request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Verification Successful.',"text1":'Go to homepage' , "link": '/'}))
#        return HttpResponse(jinja_environ.get_template('index.html').render({"pcuser":Non,
#                                                                                   "code":request.REQUEST['code']}))
#        index(request)
    try:
        request.user.pcuser
    except:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                             "text":'<p>No Pcuser associated.</p>',"text1":'<p>Please click here to go to the homepage</p>',"link":'/'}))
    
    code = request.REQUEST['code']
    pcuser = request.user.pcuser
    if pcuser.verified == '1':
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                              "text":'<p>Verification successful.</p>',"text1":'<p>Click here to go to the homepage</p>',"link":'/'}))
    elif code == pcuser.verified:
        pcuser.verified = '1'
        pcuser.save()
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                              "text":'<p>Verification successful.</p>',"text1":'<p>Click here to go to the homepage</p>',"link":'/'}))
    
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'<p>Verification Failed.</p>',"text1":'<p>Please go back or click here to go to the homepage</p>',"link":'/'}))




#Called when a user clicks login button. 
@csrf_exempt
def login_do(request):
    username = request.REQUEST['username']
    password = request.REQUEST['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            if 'redirect' in request.REQUEST.keys():
                return HttpResponse(jinja_environ.get_template('redirect.html').render({"pcuser":None,"redirect_url":request.REQUEST['redirect'].replace("!!__!!","&")}))
            return HttpResponse(jinja_environ.get_template('redirect.html').render({"pcuser":None,"redirect_url":"/"}))
            
    else:
        # Return an 'invalid login' error message.
        if "js" in request.REQUEST.keys():
            if len(User.objects.filter(username=request.REQUEST['username'])) == 0:
                return HttpResponse("inv_user")
            return HttpResponse("inv_pass")
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Invalid Login.', "text1":'Click here to go to home page.',"link":'/'}))
    
    
#Called when a user clicks logout button.
def logout_do(request):
    logout(request)
    redirect_url = "/"
    if 'redirect_url' in request.REQUEST.keys():
        redirect_url = request.REQUEST['redirect_url']
    return HttpResponse(jinja_environ.get_template('redirect.html').render({"pcuser":None,"redirect_url":redirect_url}))


#Called when a user goes to malaria track.
def malaria(request):
    all_posts = Post.objects.all()
    return HttpResponse(jinja_environ.get_template('malaria.html').render({"all_posts":all_posts, "pcuser":request.user.pcuser}))

#called when a user wants to view a particular post. Also shows up the revision history
def view_post(request):
    retval = check(request)
    if retval <> None:
        return retval

    try:
        pcuser=request.user.pcuser
        key=request.REQUEST['key']
        postobj=Post.objects.get(id=key)
        
        revpostobj = RevPost.objects.filter(owner_rev_post_id=key)
        
        return HttpResponse(jinja_environ.get_template('viewpost.html').render({"pcuser":request.user.pcuser, 'post':postobj, 'revpostobj':revpostobj}))
    except Exception as e:
        return HttpResponse(e)
    

#The call function for new post form.    
def post_form(request):
    retval = check(request)
    if retval <> None:
        return retval
    return HttpResponse(jinja_environ.get_template('newpost.html').render({"pcuser":request.user.pcuser, 'owner':request.user.pcuser}))

#Called when a user clicks submit on new post form.                                                                          
@csrf_exempt
def post_new(request):
    #check for user login
    retval = check(request)
    if retval <> None:
        return retval
    owner = request.user.pcuser
    title_post = request.REQUEST['title']
    description_post = request.REQUEST['description']
    link_post = request.REQUEST['link']
    imageobj_post = request.FILES['image_post']
    image_post = '/static/' + owner.user.username  + "post.jpg"
    
    
    entry = Post(owner=owner, 
                 title_post=title_post,
                 description_post=description_post,
                 link_post=link_post,
                 imageobj_post=imageobj_post,
                 image_post=image_post,
                 )
    entry.save()
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'Post created successfully.',"text1":'Click here to view post.', "link": '/view_post/?key=' + str(entry.id)}))

#Calls the edit post page. Also, sends the autofill form data.    
def edit_post_page(request):
    retval = check(request)
    if retval <> None:
        return retval

    try:
        pcuser=request.user.pcuser
        key=request.REQUEST['key']
        postobj=Post.objects.get(id=key)
        return HttpResponse(jinja_environ.get_template('editpost.html').render({"pcuser":request.user.pcuser, 'post':postobj}))
    except Exception as e:
        return HttpResponse(e)
    
#Called when a user edits his/her post and also saves the revision history
@csrf_exempt
def edit_post(request):
    retval = check(request)
    if retval <> None:
        return retval
    
    owner = request.user.pcuser
    postid = request.REQUEST['postid']
    postobj = None
    revpostobj = None
    try:
        postobj = Post.objects.get(pk=postid)
    except Exception as e:
        return HttpResponse(e)
    
    title_post = request.REQUEST['title']
    description_post = request.REQUEST['description']
    link_post = request.REQUEST['link']
    
    
    #To remove post picture
    if 'reset_image' in request.REQUEST.keys():
        postobj.image_post = "http://allfacebook.com/files/2012/03/bluepin.png"
        if str(postobj.imageobj_post) <> '':
            path = '/vagrant/submit/media/propics/' + owner.user.username  + "post.jpg"
            if os.path.isfile(path):
                os.remove(path)
        postobj.save()
        return edit_post(request)
    
    
    if 'image' in request.FILES.keys():
        #delete old file
        if str(postobj.imageobj_post) <> '':
            path = '/vagrant/submit/media/propics/' + owner.user.username  + "post.jpg"
            if os.path.isfile(path):
                os.remove(path)
        postobj.imageobj_post = request.FILES['image']
        postobj.image_post = '/static/' + owner.user.username  + "post.jpg"
    
    if postobj.title_post <> title_post:
        if postobj.description_post <> description_post:
            if postobj.link_post <> link_post:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=True,
                    description_change=True,
                    link_change=True,
                    )
                entry.save()
            else:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=True,
                    description_change=True,
                    link_change=False,
                    )
                entry.save()
        else:
            if postobj.link_post <> link_post:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=True,
                    description_change=False,
                    link_change=True,
                    )
                entry.save()
            else:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=True,
                    description_change=False,
                    link_change=False,
                    )
                entry.save()
            
            
    else:        
        if postobj.description_post <> description_post:
            if postobj.link_post <> link_post:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=False,
                    description_change=True,
                    link_change=True,
                    )
                entry.save()
            else:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=False,
                    description_change=True,
                    link_change=False,
                    )
                entry.save()
            
            
        else:
            if postobj.link_post <> link_post:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=False,
                    description_change=False,
                    link_change=True,
                    )
                entry.save()
            else:
                entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                    title_post_rev=postobj.title_post,
                    description_post_rev=postobj.description_post,
                    link_post_rev=postobj.link_post,
                    title_change=False,
                    description_change=False,
                    link_change=False,
                    )
                entry.save()
                
        
    
    
    postobj.title_post = title_post
    postobj.description_post = description_post
    postobj.link_post = link_post
    
    postobj.save()
    
    postobj.owner.save()
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'Post edited successfully.',"text1":'Click here to view post.', "link": '/view_post/?key=' + str(postobj.id)}))



#Called when a user cancels his post. 
@csrf_exempt
def delete_post(request):
    retval = check(request)
    if retval <> None:
        return retval
    user = request.user

    postid = request.REQUEST['postid']
        
    postobj = None
    try:
        postobj = Post.objects.get(pk=postid)
    except Exception as e:
        return HttpResponse(e)
    
    postobj.delete()

    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'Post Deleted successfully.', "text1":'Click here to go to home page.',"link":'/'}))

#Call to open user's profile page.Sends data to be displayed.        
def profile(request):
    
    try:
        pcuserid = request.REQUEST['id']
        if pcuserid == request.user.pcuser.pk:
            return HttpResponse(jinja_environ.get_template('profile.html').render({"pcuser":request.user.pcuser, "profiler":request.user.pcuser}))
        else:
            return HttpResponse(jinja_environ.get_template('profile.html').render({"pcuser":request.user.pcuser, "profiler":Pcuser.objects.get(pk=pcuserid)}))
    except:
        return HttpResponse(jinja_environ.get_template('profile.html').render({"pcuser":request.user.pcuser, "profiler":request.user.pcuser}))


#Calls the edit profile page. The autofill data is sent too.
def edit_profile_page(request):
    if not request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('index.html').render({"pcuser":None}))
    pcuserid = request.REQUEST['id']
    return HttpResponse(jinja_environ.get_template('edit_profile.html').render({"pcuser":Pcuser.objects.get(pk=pcuserid)}))

#Edit profile function. Called after a user presses done in edit profile. New data is requested from frontend and stored.
@csrf_exempt
def edit_profile(request):
    if not request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('index.html').render({"pcuser":None}))

    
    #To remove profile picture
    if 'reset_image' in request.REQUEST.keys():
        request.user.pcuser.image = "http://vfcstatic.r.worldssl.net/assets/car_icon-e0df962a717a5db6ebc8b37e80b05713.png"
        if str(request.user.pcuser.imageobj) <> '':
            path = '/vagrant/submit/media/propics/' + request.user.username + request.user.pcuser.imageobj.url[request.user.pcuser.imageobj.url.rfind('.'):]
            if os.path.isfile(path):
                os.remove(path)
        request.user.pcuser.save()
        return edit_profile_page(request)
    
    
    if 'image' in request.FILES.keys():
        #delete old file
        if str(request.user.pcuser.imageobj) <> '':
            path = '/vagrant/submit/media/propics/' + request.user.username + ".jpg"
            if os.path.isfile(path):
                os.remove(path)
        request.user.pcuser.imageobj = request.FILES['image']
        request.user.pcuser.image = '/static/' + request.user.username + ".jpg"
    
    
    
    
    
    
    request.user.pcuser.gender = request.REQUEST['gender']
    request.user.pcuser.phone = request.REQUEST['phone']
    request.user.pcuser.phone = request.REQUEST['email']
    request.user.pcuser.gender = request.REQUEST['location']
    request.user.first_name = request.REQUEST['first_name']
    request.user.last_name = request.REQUEST['last_name']
    
    request.user.pcuser.save()
    
    request.user.save()
    
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'Profile edit successful.',"text1":'Click here to view the profile.',"link":'/profile/?id='+ str(request.user.pcuser.id)}))

#Forgot Password page call function.
def forgot_pass_page(request):
    if request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                              "text":'<p>Please log out before requesting reset in password.</p>\
                                                                                  <p>Click OK to go to the homepage</p>',"link":'/'}))
    return HttpResponse(jinja_environ.get_template('forgot_password.html').render({"pcuser":None}))




#Called when the user clicks forgot password after the data is validated. This sends a verification mail to the user.
@csrf_exempt
def forgot_pass(request):
    if request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'<p>Please log out in order to request for a password reset.</p>\
                                                                                  <p>Please go back or click here to go to the homepage</p>',"link":'/'}))
    if 'username' not in request.REQUEST.keys() or 'email' not in request.REQUEST.keys():
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Invalid Request. Please go back or',"text1":'click here to go to the homepage',"link":'/'}))
    user = User.objects.filter(username=request.REQUEST['username'])
    if len(user) == 0:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'User Does not exist. Please go back or',"text1":'click here to go to the homepage',"link":'/'}))
    user = user[0]
    if user.email <> request.REQUEST['email']:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Invalid email. Please go back or',"text1":'click here to go to the homepage',"link":'/'}))
    user.pcuser.reset_pass = uuid.uuid4().hex
    user.pcuser.save()
    
    subject = "Password Reset Request"
    msg = 'Subject: %s \n\nYou have requested for a password reset on Mobile App Control Center\n\
    Please click on the following link (or copy paste in your browser) to reset your password.\n\n\
    %s/reset_pass_page/?reset_pass=%s&email=%s\n\n\
    If you have not requested for a reset of password, please ignore.' % (subject, website, user.pcuser.reset_pass, user.email)
    
    x = send_email(msg, user.email)
    if x[0] == 0:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Could not process request, please try again later by going back or',"text1":'clicking here to go to the homepage', "link":'/'}))
    else:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'<p>An email has been sent to your regestered email address.</p>\
                                                                                  <p>Check your email and click on the link to reset your password.</p>',"text1":'<p>Click here to go to the homepage</p>',"link":'/'}))
    

    
#Reset Password page call function.
@csrf_exempt
def reset_pass_page(request):
    if request.user.is_authenticated():
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                              "text":'<p>Please log out before requesting reset in password.</p>',"text1":'<p>Click here to go to the homepage</p>',"link":'/'}))
    if "reset_pass" not in request.REQUEST.keys() or 'email' not in request.REQUEST.keys():
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'<p>Invalid Request</p>',"text1":'Click here to go to the homepage</p>', "link":'/'}))
    reset_pass = request.REQUEST['reset_pass']
    if reset_pass == "":
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'<p>Invalid Request</p>',"text1":'<p>click here to go to the homepage</p>', "link":'/'}))
    user = Pcuser.objects.filter(reset_pass=reset_pass)
    if len(user)==0:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                                "text":'Invalid Request.',"text1":'Please go back or click here to go to the homepage',"link":'/'}))
    
    user = user[0].user
    
    if user.email <> request.REQUEST['email']:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                                "text":'Invalid Email.',"text1":'Please go back or click here to go to the homepage',"link":'/'}))
    return HttpResponse(jinja_environ.get_template('reset_password.html').render({'pcuser':None, 'reset_pass':reset_pass}))



#Called when the user clicks change password button. Checks if the previous password is valid or not.
@csrf_exempt
def change_pass(request):
    if "reset_pass" in request.REQUEST.keys():
        reset_pass = request.REQUEST['reset_pass']
        if reset_pass == "":
            return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                                  "text":'<p>Invalid Request</p>', "text1":'<p>click here to go to the homepage</p>',"link":'/'}))
        user = Pcuser.objects.filter(reset_pass=reset_pass)
        if len(user)==0 or 'pass' not in request.REQUEST.keys():
            return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                                  "text":'Invalid Request.',"text1":'Please go back or click here to go to the homepage',"link":'/'}))
        user = user[0].user
        user.set_password(request.REQUEST['pass'])
        user.save()
        user.pcuser.reset_pass = ""
        user.pcuser.save()
        logout(request)
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Password Changed.',"text1":'Please click here to go to the homepage and log in again.',"link":'/logout_do/'}))
    else:
        retval = check(request)
        if retval <> None:
            return retval
        if "pass" not in request.REQUEST.keys() or "oldpass" not in request.REQUEST.keys():
            return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                                  "text":'Invalid Request.', "text1":'Please go back or click here to go to the homepage',"link":'/'}))
        if not request.user.check_password(request.REQUEST['oldpass']):
            return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                                  "text":'Invalid Old Password.',"text1":'Click here to go to the homepage',"link":'/'}))
        request.user.set_password(request.REQUEST['pass'])
        request.user.save()
        logout(request)
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                              "text":'Password Changed.',"text1":'Please click here to go to the homepage and log in again.',"link":'/logout_do/'}))
    
    
    
#Change password page call function    
def change_pass_page(request):
    retval = check(request)
    if retval <> None:
        return retval
    return HttpResponse(jinja_environ.get_template('change_password.html').render({"pcuser":request.user.pcuser}))
        
    


#called when user wishes to go to the Peacetrack from dashboard
def peacetrack(request):
    return HttpResponse(jinja_environ.get_template('peacetrack.html').render({"pcuser":None}))  



#Called when a user wants to see the details of a volunteer.
def volunteer(request):
    all_vol = Volunteer.objects.all()
    return HttpResponse(jinja_environ.get_template('volunteer.html').render({"all_vol":all_posts, "pcuser":request.user.pcuser}))


#called when user wishes to go to the Peacetrack from dashboard
def aboutPC(request):
    return HttpResponse(jinja_environ.get_template('aboutPC.html').render({"pcuser":None}))  

#called when user wishes to go to the Peacetrack from dashboard
def policies(request):
    return HttpResponse(jinja_environ.get_template('policies.html').render({"pcuser":None}))  

#called when user wishes to go to the Peacetrack from dashboard
def details(request):
    return HttpResponse(jinja_environ.get_template('details.html').render({"pcuser":None}))  

#called when user wishes to go to the Peacetrack from dashboard
def helpPC(request):
    return HttpResponse(jinja_environ.get_template('helpPC.html').render({"pcuser":None}))  


