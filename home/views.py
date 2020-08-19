from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('This is home1')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, 'Please fill the details Correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your Message sent')
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContains = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContains)
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found, please refine your query.')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken please try again with another Username')
                return redirect('home')
            if len(username) > 10 and not username.isalnum():
                messages.error(request, 'Username must be under 10 characters and contain letters and characters only')
                return redirect('home')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email taken please try again with different Email Address')
                return redirect('home')

        else:
            messages.error(request, 'Password do not match')
            return redirect('home')

        myuser = User.objects.create_user(username=username, email=email,first_name=fname,last_name=lname,password=pass1)
        myuser.save()
        messages.success(request, 'Account created successfully')
        return redirect('home')

    else:
        return HttpResponse('404 - Not found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername,password=loginpass)

        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials, please try again')
            return redirect('home')
    return HttpResponse('404 - Not found')

def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Loggd Out')
    return redirect('home')


