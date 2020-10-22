from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from auctions.models import Categorie, Listing, Comment, Wishlist
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

class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Write a comment', 
        widget=forms.Textarea(attrs={
            'class': '',
            'placeholder': 'Write here!',
            'rows': '4',
            'columns': '50',
        }))

def index(request):
    listings = Listing.objects.all()
    active_listings = [listing for listing in listings if listing.is_active]
    return render(request, "auctions/index.html", {
        "listings": active_listings,
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

# ACCOUNT FOR NULL OPTION IN THE FORM
# MODIFY MODEL USING https://docs.djangoproject.com/en/dev/ref/forms/fields/#modelchoicefield

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


def listing_entry(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing_name=listing)
    # tentar entrar nessa página sem um usuário logado provavelmente vai quebrar a página
    # para consertar, eu sugiro um check para verificar se o usuário está autenticado
    wishlist = Wishlist.objects.get(user_id=request.user.id)
    items_in_wishlist = wishlist.items.all()
    if listing in items_in_wishlist:
        in_wishlist = "Remove from wishlist"
    else:
        in_wishlist = "Add to wishlist"
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "commentForm": CommentForm(),
        "comments": comments,
        "wishlist": in_wishlist,
    })

@login_required
def commenting(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        user = User.objects.get(pk=int(request.user.id))
        listing = Listing.objects.get(pk=int(listing_id))
        commentFile = Comment(listing_name=listing, user_name=user, comment=comment)
        commentFile.save()
        return HttpResponseRedirect(reverse("listing_entry", args=(listing_id,)))

@login_required
def wishlist(request, listing_id):
    user = request.user
    # tris to get the user's list
    try:
        wishlist = Wishlist.objects.get(user_id=user.id)
    # if it does not exist
    except DoesNotExist:
        # creates the list and saves it to a variable
        Wishlist.objects.create(user_id=user.id)
        wishlist = Wishlist.objects.get(user_id=user.id)
    # gets all the items in the list
    items_in_wishlist = wishlist.items.all()
    # gets the current item the user is viewing
    item_at_hand = Listing.objects.get(pk=listing_id)
    # if the item is in the list
    if item_at_hand in items_in_wishlist:
        # it removes it
        wishlist.items.remove(item_at_hand)
    else:
        # else, adds it
        wishlist.items.add(item_at_hand)
        # returns to the listing page
    return HttpResponseRedirect(reverse("listing_entry", args=(listing_id,)))

@login_required
def wishlist_page(request):
    user = request.user
    wishlist = Wishlist.objects.get(user_id=user.id)
    wishlist_items = wishlist.items.all()
    return render(request, "auctions/watchlist.html", {
        "wishlist_items": wishlist_items,
    })