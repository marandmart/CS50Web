from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Post, Follow

# function used to retrieve posts
def all_posts(user=""):
    # if there's a user parameter passed
    if user:
        # retrives all posts from the user(s)
        posts = Post.objects.filter(user=user)
    else:
        # if there were no parameters, returns all posts
        posts = Post.objects.all()
    # puts the posts in reverse chronological order
    posts = posts[::-1]
    return posts

def index(request):
    # gets all posts
    posts = all_posts()
    return render(request, "network/index.html", {
        "posts": posts
    })

def profile(request, user_id):
    # gets the user info
    user = User.objects.get(pk=user_id)
    # gets the user's posts
    posts = all_posts(user=user)
    # gets the user's follows and followers
    follow = Follow.objects.get(user=user)
    return render(request, "network/profile.html", {
        "posts": posts,
        "user": user,
        "follow": follow,
    })

def following(request):
    # gets all the accounts the user follows
    follows = Follow.objects.get(user=request.user).following.all()
    # gets all the post from those accounts in reverse chronological order
    posts = Post.objects.filter(user__in=follows)[::-1]
    return render(request, "network/following.html", {
        "posts": posts,
    })
    

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            follow_list = Follow.objects.create(user=user)
            follow_list.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        post = request.POST["post"]
        time = datetime.now()
        new_post = Post(user=user, post=post, time=time)
        new_post.save()
    return HttpResponseRedirect(reverse("index"))

