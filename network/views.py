import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Author, Like


def index(request):
    posts = Post.objects.order_by("-created_at").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@csrf_exempt
@login_required
def create_post(request):
    text = request.POST.get('new-post')
    new_post = Post(text=text, user=request.user)
    new_post.save()
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def update_post(request, post_id):
    data = json.loads(request.body)
    print(data)
    new_text = data.get("text")
    post = Post.objects.get(pk=post_id)
    post.text = new_text
    post.save()
    return JsonResponse(post.serialize(), status=201)


@login_required
def like_post(request, post_id, type):
    post = Post.objects.get(pk=post_id)
    num_likes = len(post.post_likes.all())
    print(num_likes)
    try:
        like = Like.objects.get(post=post, user=request.user)
    except Like.DoesNotExist:
        like = False
    if type == "unlike" and like:
        like.delete()
        num_likes -= 1
    elif type == "like" and not like:
        new_like = Like(post=post, user=request.user)
        new_like.save()
        num_likes =+ 1
    return JsonResponse({
        "num_likes": num_likes,
    }, status=201)


@csrf_exempt
@login_required
def change_follow(request):
    data = json.loads(request.body)
    value = data.get("value")
    author_name = data.get("author")
    author = Author.objects.get(user=User.objects.get(username=author_name))
    if value == "follow":
        author.followers.add(User.objects.get(pk=request.user.id))
    elif value == "unfollow":
        author.followers.remove(User.objects.get(pk=request.user.id))
    return JsonResponse({
        "followers": len(author.followers.all()),
        "following": len(author.user.followed_authors.all())
    }, status=201)


@login_required
def following(request):
    posts = Post.objects.filter(user__in=[author.user for author in request.user.followed_authors.all()]).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


def profile(request, username):
    user = User.objects.get(username=username)
    author = Author.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "author": author
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
            author = Author.objects.create(user=user)
            author.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
