from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow

# PAGINA QUEBRA QUANDO O USUÁRIO NÃO ESTÁ LOGADO

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

def index(request, page_number=""):
    # gets all posts
    objects = all_posts()
    # splits the posts into pages
    posts = Paginator(objects, 10)
    # if a page_number was passed, retrieves that page number
    if page_number:
        page = posts.page(int(page_number))
    # else returns page 1
    else:
        page = posts.page(1)
    return render(request, "network/index.html", {
        "posts": page
    })

def profile(request, user_id, page_number=""):
    # gets the user's info
    user = User.objects.get(pk=user_id)
    # gets the user's posts
    objects = all_posts(user=user)
    # uses the paginator function to distribute the content
    posts = Paginator(objects, 10)
    # if a page_number was passed, retrieves that page number
    if page_number:
        page = posts.page(int(page_number))
    # else returns page 1
    else:
        page = posts.page(1)
    # gets the user's follows and followers
    follow_data = Follow.objects.get(user=user)
    if request.user != user and request.user.is_authenticated:
        this_user = User.objects.get(pk=request.user.id)
        follows_this_user = user in this_user.follow_status.following.all()
        return render(request, "network/profile.html", {
            "posts": page,
            "user": user,
            "follow": follow_data,
            "follow_status": follows_this_user,
        })
    return render(request, "network/profile.html", {
        "posts": page,
        "user": user,
        "follow": follow_data,
    })

def following(request, page_number=""):
    # gets all the accounts the user follows
    follows = Follow.objects.get(user=request.user).following.all()
    # gets all the post from those accounts in reverse chronological order
    objects = Post.objects.filter(user__in=follows)[::-1]
    # splits the posts into pages
    posts = Paginator(objects, 10)
    # if a page_number was passed, retrieves that page number
    if page_number:
        page = posts.page(int(page_number))
     # else returns page 1
    else:
        page = posts.page(1)
    return render(request, "network/following.html", {
        "posts": page,
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

@csrf_exempt
@login_required
def follow_unfollow(request, user_id):
    # checks if it's a PUT request
    if request.method == "PUT":
        # get the id of the user making the request
        user_following = User.objects.get(pk=request.user.id)
        # gets the id of the user receiving the follower
        user_followed = User.objects.get(pk=user_id)
        # load in the data for the request
        data = json.loads(request.body)
        # if the current followStatus is false, it means the requesting user is trying to follow this user
        if data.get("followStatus") == "False":
            # adds this user to the follow list of the request user
            user_following.follow_status.following.add(user_followed)
            # adds the request user to the followers list of the user
            user_followed.follow_status.followers.add(user_following)
        # else if the current followStatus is true, it means the requesting user is trying to unfollow this user
        elif data.get("followStatus") == "True":
            # removes this user to the follow list of the request user
            user_following.follow_status.following.remove(user_followed)
            # removes the request user to the followers list of the user
            user_followed.follow_status.followers.remove(user_following)
        # returns a no content response
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method == "PUT":
        # gets the post using the post id
        post = Post.objects.get(pk=post_id)
        # loads in the data from the fetch request
        data = json.loads(request.body)
        # saves the loaded content to the post
        post.post = data.get("edit")
        # saves the changes
        post.save()
        # return a no content response
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        })

@csrf_exempt
@login_required
def like_dislike(request, post_id):
    if request.method == "PUT":
        # gets the user data
        user = User.objects.get(pk=request.user.id)
        # gets the post data
        post = Post.objects.get(pk=post_id)
        # gets the fetch data
        data = json.loads(request.body)
        # saves the like info
        like = data.get("like")
        # saves the dislike info
        dislike = data.get("dislike")
        # does the proper adding or removal of the user from liking/disliking the post
        if like == "true":
            post.likes.add(request.user)
        elif like == "false":
            post.likes.remove(request.user)
        if dislike == "true":
            post.dislikes.add(request.user)
        elif dislike == "false":
            post.dislikes.remove(request.user)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        })