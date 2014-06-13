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
from webhub.serializers import UserSerializer
import smtplib

#SMTP port for sending emails
SMTP_PORT = 465

#link for the localhost
website = "http://192.168.33.10:8000"

jinja_environ = jinja2.Environment(loader=jinja2.FileSystemLoader(['ui']), extensions=[loopcontrols])


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
    
    

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
                                                                              "text":'<p>Username already exists. Please enter some other username.</p><p>Go Back or click OK to go to signup page.</p>',"link":'/signup_page/'}))
    

    
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
                                                                              "text":'Verification Successful. Go to homepage' , "link": '/'}))
#        return HttpResponse(jinja_environ.get_template('index.html').render({"pcuser":Non,
#                                                                                   "code":request.REQUEST['code']}))
#        index(request)
    try:
        request.user.pcuser
    except:
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":None,
                                                                             "text":'<p>No Pcuser associated.</p><p>Please go back or click OK to go to the homepage</p>',"link":'/'}))
    
    code = request.REQUEST['code']
    pcuser = request.user.pcuser
    if pcuser.verified == '1':
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                              "text":'<p>Verification successful.</p><p>Click OK to go to the homepage</p>',"link":'/'}))
    elif code == pcuser.verified:
        pcuser.verified = '1'
        pcuser.save()
        return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                              "text":'<p>Verification successful.</p><p>Click OK to go to the homepage</p>',"link":'/'}))
    
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'<p>Verification Failed.</p><p>Please go back or click OK to go to the homepage</p>',"link":'/'}))




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
    
    entry = Post(owner=owner, 
                 title_post=title_post,
                 description_post=description_post,
                 )
    entry.save()
    return HttpResponse(jinja_environ.get_template('notice.html').render({"pcuser":request.user.pcuser,
                                                                          "text":'Post successful.',"text1":'Click here to go to home.',
                                                                          "link": '/'}))

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
    
    entry = RevPost(owner_rev=owner, 
                    owner_rev_post=postobj, 
                 title_post_rev=postobj.title_post,
                 description_post_rev=postobj.description_post,
                 )
    entry.save()
    
    title_post = request.REQUEST['title']
    description_post = request.REQUEST['description']
    
    
    postobj.title_post = title_post
    postobj.description_post = description_post
    
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

