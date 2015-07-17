import jinja2
import smtplib
import uuid
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from jinja2.ext import loopcontrols
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from webhub import xlrd
from webhub.checker import check
from webhub.models import *
from webhub.serializers import *


# SMTP port for sending emails
SMTP_PORT = 465

#link for the localhost
website = "http://systerspcweb.herokuapp.com/"

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
    gmailLogin = 'pc.mobile.control.center'
    gmailPas = 'alphadeltaepsilon'
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
    request.user.pcuser.email = request.REQUEST['email']
    request.user.pcuser.location = request.REQUEST['location']
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
        

#called when user wishes to go to the about PeaceCorps
def aboutPC(request):
    return HttpResponse(jinja_environ.get_template('aboutPC.html').render({"pcuser":None}))  

#called when user wishes to go to the Policies
def policies(request):
    return HttpResponse(jinja_environ.get_template('policies.html').render({"pcuser":None}))  

#called when user wishes to go to the Important details
def details(request):
    return HttpResponse(jinja_environ.get_template('details.html').render({"pcuser":None}))  

#called when user wishes to go to the Help
def helpPC(request):
    return HttpResponse(jinja_environ.get_template('helpPC.html').render({"pcuser":None}))  

#called to test if the script is fetching data from the excel sheet
def testDB(request):
    book = xlrd.open_workbook("Updated Project Framework Indicator List PeaceTrack.xlsx")
    no = book.nsheets
    
    return HttpResponse(jinja_environ.get_template('test.html').render({"pcuser":None, "no":no}))  

