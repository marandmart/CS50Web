from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from auctions.models import Categorie, Listing
from .models import User

# form for creating a new listing
class ListingForm(forms.Form):
    title = forms.CharField(
        label='Title', 
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter a title for the listing',
        }))
    description = forms.CharField(
        label='Description', 
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a description',
            'rows': '5',
            'columns': '60',
        }))
    img_url = forms.URLField(
        label='Image URL', 
        required=False, 
        widget=forms.URLInput(attrs={
            'class': 'form-group col-md-6',
            'placeholder': 'URL for the item image',
        }))
    price = forms.DecimalField(
        label="Item's price", 
        decimal_places=2, 
        max_digits=10,
        min_value=0, 
        widget=forms.NumberInput(attrs={
            'class': 'form-group col-md-1',
            'placeholder': 'Price',
        }))

def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    categories = Categorie.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        img_url = request.POST["img_url"]
        price = request.POST["price"]
        category = Categorie.objects.get(pk=int(request.POST["category"]))
        user = User.objects.get(pk=request.user.id)
        listing = Listing(title=title, description=description, image_URL=img_url, price=price, category=category, user=user)
        listing.save()
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm(),
            "categories": categories,
            "message": "Listing created succefully!",
        })
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm(),
        "categories": categories,
    })