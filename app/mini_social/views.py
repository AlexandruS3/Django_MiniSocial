# views module
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect
from random import randint
import random
from .models import Comment, Post, CustomUser
#from django.contrib.auth.models import CustomUser
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
import re
from django.contrib.sessions.models import Session
 

# AKA DATABASE

users = [
    {"username": "johny", "created": "2000-01-01"},
    {"username": "marry", "created": "2000-01-02"},
    {"username": "pete", "created": "2000-01-03"},
    {"username": "pier", "created": "2000-01-04"},
    {"username": "vasilyi", "created": "2000-01-05"},
    {"username": "masha", "created": "2000-01-06"},
    {"username": "lily", "created": "2000-01-07"},
]

posts = [
    {"title": "First title", "created":"2001-01-01"},
    {"title": "Second title", "created":"2001-01-02"},
    {"title": "Third title", "created":"2001-01-03"},
    {"title": "Fourth title", "created":"2001-01-04"},
    {"title": "Fifth title", "created":"2001-01-05"},
    
]


def homePage(request):
    template = loader.get_template("home.html")
    show_notifications = request.session.get('show_notifications', None)
    return HttpResponse( template.render({
        "last_users":users[:5],
        "last_posts":posts[:3],
        "user": request.user,
        "show_notifications" : show_notifications
        }, request))


def signupPage(request):
    template = loader.get_template("signup.html")

    return HttpResponse( template.render({
    }, request))

def profilePage(request):
    return HttpResponse("User's page")

def postsPage(request): 
    return HttpResponse("Post's page")

    

# COMMENT VIEWS 
     
def saveComment(request):
    if request.method == 'POST':
        visitingUser = get_user(request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)
        post_id = request.POST['post_id'] 
       
        post = Post.objects.get(pk=post_id)

        body  = request.POST['body']

        comment = Comment(body=body, post=post, author=visitingUser)
        comment.save()
        return redirect (f'/post/page/{post_id}')
    else:
        return HttpResponseForbidden('Acces Denied')
    
# POST VIEWS
def addPost(request):
    # HW1: check if user is authenticated
    if request.user.is_authenticated:
        template = loader.get_template("post/add.html")
        return HttpResponse( template.render({
            }, request))
    else:
        return HttpResponseForbidden('Acces Denied')


#             data
#               v
def savePost(request):  # HttpRequest
  
        visitingUser = get_user(request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)

        title = request.POST['title']
        body  = request.POST['body']

        post = Post(title=title , body=body , author=visitingUser)
        post.save()

        # HW2: redirect ot it's profile
        return redirect (f'/user/profile/{visitingUser.id}')
     




def getPosts(request):
    template = loader.get_template("post/get.html")

    posts = Post.objects.all()

    print(type(posts)) # QuerySet
    return HttpResponse( template.render({
        'posts': posts
        }, request))


def showPost(request,id):
    template = loader.get_template("post/page.html")
    
    # 1. find the post by id
    comment = Comment.objects.all()
    post = Post.objects.get(pk=id)
    return HttpResponse( template.render({
        'post': post,
        'comment': comment
         
        }, request))



    

def updatePost(request):
    template = loader.get_template("post/update.html")
    id = request.GET['id']

    # 1. find the post by id
    post = Post.objects.get(pk=id)
    return HttpResponse( template.render({
        'post': post 
        }, request))






def deletePost(request):

    id = request.GET['id']

    # 1. find the post by id
    post = Post.objects.get(pk=id)

    # 2. delete post
    post.delete()
    return HttpResponse ('Post deleted succesfully')



def changePost(request):
 
    id = request.GET['id']
    new_title = request.GET['title']
    new_body = request.GET['body']

    # 1. find the post by id
    post = Post.objects.get(pk=id)

    post.title = new_title
    post.body = new_body


    post.save()

    return HttpResponse("Post updated succesfully")


# USER VIEWS
def registerUser(request):
    if request.method =='GET' :
        template = loader.get_template("user/register.html")
        return HttpResponse( template.render({}, request))
    
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        def check_alphanumeric(username):
            return bool(re.match(r'^[a-zA-Z0-9]+$', username))
        
        if len(username) < 5 or len(username) >= 12:
            messages.success(request,'the user name must contain at least 5 and at most 12 characters ', extra_tags='lennn')
            return redirect ("/user/register")

        
        if check_alphanumeric(username) != True:
            messages.success(request,'username must contain latin letters and numbers ', extra_tags='abecedar')
            return redirect ("/user/register") 
        
        
        if "a" and "." not in email:
            messages.success(request,'invalid format for mail', extra_tags='mail')
            return redirect ("/user/register") 
        
        if password != confirm_password:
            messages.success(request,'Passwords do not match!' )
            return redirect ("/user/register") 
        
        user = CustomUser.objects.create_user(username, email, password)

        #if user is not None:
        #    # Authenticate the user
        #    user = authenticate(username=username, password=password)
        #    if user is not None:
        #        # Log in the user
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect("/")

    



def loginUser(request):
    # req -----> Form
    if request.method =='GET' :
        template = loader.get_template("user/login.html")
        #message = request.session.get('error_message', None)
        return HttpResponse( template.render({}, request))
    
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password= password)
    # req -----> Auth   

        if user is None:
            #request.session['error_message'] = 'Wrong credentials!'
            messages.error(request,'Wrong credentials!' )
            return redirect ("/user/login") 
        
    
        login(request, user)
        #request.session.pop('error_message')
        visitingUser = CustomUser.objects.get(pk=user.id)
        # 1. load the backup data

        session_data_backup = visitingUser.session_data_backup
        session_data = json.loads(session_data_backup if session_data_backup else '{}')

        # 2. put the data in current session
        request.session.update(session_data)

        

        
        messages.success(request,'Login succesful!')
        return redirect ("/") 
    #messages.add_message(request, messages.INFO, "Over 9000!", extra_tags="dragonball")



def toggleUserNotification(request):
    visitingUser = get_user(request)
    toggle = request.GET.get('toggle', None)
    # .POST.get()
    if not toggle:
        request.session['show_notifications'] = False
    else:
        request.session['show_notifications'] = True
        
    return redirect(f"/user/profile/{visitingUser.id}")



import json


def logoutUser(request): 

    visitingUser = get_user(request)
    visitingUser = CustomUser.objects.get(pk=visitingUser.id)

    # 1. get all the current session data
    session = Session.objects.get(pk=request.session.session_key)
    session_data = session.get_decoded()

    # 2. serialize data in json
    session_data_json = json.dumps(session_data)

    # 3. save to backup column in visiting user
    visitingUser.session_data_backup = session_data_json
    visitingUser.save()


    #show_notifications = request.session.get('show_notifications', None)
    logout(request) # session.flush()
    #request.session['show_notifications'] = show_notifications
    #messages.success(request,'LogOut succesful!',extra_tags='dragonball')
    


    return redirect("/")



     
def userProfile(request, id):
    # req -----> Form
    if request.method =='GET' :
        profileUser = CustomUser.objects.get(pk=id)
        show_notifications = request.session.get('show_notifications', None)
        visitingUser = get_user(request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)
        template = loader.get_template("user/profile.html")
        userFriend = profileUser.friends.all()
        posts = Post.objects.all() #HW3 

        profileUserIsNotVisitingUserFriend = visitingUser.friends.all().contains(profileUser)
        #message = request.session.get('error_message', None)
        return HttpResponse( template.render({
            'profileUser': profileUser,
            'visitingUser': visitingUser,
            'userFriends' : userFriend,
            'posts' : posts,       #HW3
            'profileUserIsNotVisitingUserFriend': profileUserIsNotVisitingUserFriend,
            'show_notifications' : show_notifications
        }, request))
    
def editUserProfile(request, id):
    # req -----> Form
    if request.method =='GET' :
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user(request)
        if profileUser.id == visitingUser.id:
            template = loader.get_template("user/edit-profile.html")
            #message = request.session.get('error_message', None)
            return HttpResponse( template.render({
                'profileUser': profileUser,
            }, request))
        else:
            return HttpResponseForbidden('Acces Denied')
        
    elif request.method =='POST' :
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user(request)
        if profileUser.id == visitingUser.id:
            avatar = request.FILES['avatar'] # this file is still in MEMORY!!!
            avatar_file = open(f'app/public/uploads/{avatar}', 'wb+')
            for chunk in avatar.chunks():
                avatar_file.write(chunk)
            avatar_file.close()
            profileUser.avatar = f'uploads/{avatar}'
            profileUser.save()
            return redirect (f'/user/profile/{profileUser.id}')
        
        else:
            return HttpResponseForbidden('Acces Denied')
        

     
def addUserFriend(request, id):
    # req -----> Form
    if request.method =='GET' :
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user(request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)

        visitingUser.friends.add(profileUser)
        visitingUser.save()
        
        return redirect (f"/user/profile/{profileUser.id}")
    

    # HW: finsih "remove from friends"


def deleteUserFriend(request, id):
    # req -----> Form
    if request.method =='GET' :
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user(request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)

        visitingUser.friends.remove(profileUser)
        visitingUser.save()
        
        return redirect (f"/user/profile/{visitingUser.id}")












   #    if user is None:
   #        #request.session['error_message'] = 'Wrong credentials!'
   #        messages.error(request,'Wrong credentials!' )
   #        return redirect ("/user/login") 
   #    
   #
   #    login(request, user)
   #    #request.session.pop('error_message')
   #    messages.success(request,'Login succesful!')
   #    return redirect ("/") 
   ##messages.add_message(request, messages.INFO, "Over 9000!", extra_tags="dragonball")

