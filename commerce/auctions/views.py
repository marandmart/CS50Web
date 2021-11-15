from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from auctions.models import Categorie, Listing, Comment, Wishlist, Bid, Winner
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
            'columns': '90',
        }))

def index(request):
    # gets all listings
    listings = Listing.objects.all()
    # empty bid list
    bids =[]
    # creates a list with all active listings
    active_listings = [listing for listing in listings if listing.is_active]
    # checks which listings have active bids
    for listing in active_listings:
        try:
            bids.append(Bid.objects.get(listing=listing))
        # if they don't have bids, add an empty string to keep order
        except Bid.DoesNotExist:
            bids.append("")
    # reverses it so that the most recent listings will show up on top
    active_listings = active_listings[::-1]
    bids = bids[::-1]
    # creates a dictionary with each listing and their corresponding bid
    listings_bids = {active_listings[i]: bids[i] for i in range(len(active_listings))}
    return render(request, "auctions/index.html", {
        "listings_bids": listings_bids,
    })

def inactive(request):
    # gets all the listing objects
    listings = Listing.objects.all()
    # saves all the inactive ones
    inactive_listings = [listing for listing in listings if (not listing.is_active)]
    # renders them as a list
    return render(request, "auctions/all_inactive_listings.html", {
        "inactive_listings": inactive_listings,
    })

def inactive_listing(request, listing_id, message=""):
    # gets the listing info
    listing = Listing.objects.get(pk=listing_id)
    try:
        # checks if there was winner
        winner_info = Winner.objects.get(listing=listing)
    except:
        # saves an empty string if there wasn't
        winner_info = ""
    # gets the comments
    comments = Comment.objects.filter(listing_name=listing)
    # renders the page for the inactive listing entry
    return render(request, "auctions/inactive_listing.html", {
            "listing": listing,
            "comments": comments,
            "winner": winner_info,
            "message": message,
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
    # gets the categories available on the site
    categories = Categorie.objects.all()
    # checks if the request method is POST
    if request.method == "POST":
        # gets the new listing's info
        title = request.POST["title"]
        description = request.POST["description"]
        img_url = request.POST["img_url"]
        price = request.POST["price"]
        try:
            category = Categorie.objects.get(pk=int(request.POST["category"]))
        except Categorie.DoesNotExist:
            category = None
        user = User.objects.get(pk=request.user.id)
        listing = Listing(title=title, description=description, image_URL=img_url, price=price, category=category, user=user)
        # saves the listing info
        listing.save()
        # returns the user to the "create a listing" page with a message that the listing was created succesfully
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm(),
            "categories": categories,
            "message": "Listing created succefully!",
        })
    # if the user isn't creating an entry, it shows the regular "create a listing" form
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm(),
        "categories": categories,
    })

def listing_entry(request, listing_id, message=""):
    # listing info
    listing = Listing.objects.get(pk=listing_id)
    # comments
    comments = Comment.objects.filter(listing_name=listing)
    # tries to get the bid value if they exist
    try:
        bid = Bid.objects.get(listing=listing)
    # if they don't exist, bid gets an empty string so it won't break the page
    except Bid.DoesNotExist:
        bid = ""
    #if the user user is authenticated
    if request.user.is_authenticated:
        # tries to get the user's wishlist info
        try:
            wishlist = Wishlist.objects.get(user_id=request.user.id)
        # if the user doesn't have a wishlist, one is created for them
        except Wishlist.DoesNotExist:
            # creates a wishlist for the user 
            Wishlist.objects.create(user_id=request.user.id)
            # and then attaches it to a variable
            wishlist = Wishlist.objects.get(user_id=request.user.id)
        # gets all the items in the wishlist
        items_in_wishlist = wishlist.items.all()
        # if the listing item is in the wishlist, it gives the option to remove it
        if listing in items_in_wishlist:
            in_wishlist = "Remove from wishlist"
        # else it gives the option to add it
        else:
            in_wishlist = "Add to Wishlist"
        # renders the page with the proper information for an authenticated user
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "commentForm": CommentForm(),
        "comments": comments,
        "wishlist": in_wishlist,
        "bid": bid,
        "message": message,
    })
    # loads the page with the info for a non authenticated user
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "commentForm": CommentForm(),
        "comments": comments,
        "bid": bid,
    })

@login_required
def commenting(request, listing_id):
    # checks the request method
    if request.method == "POST":
        # saves the content of the comment
        comment = request.POST["comment"]
        # gets the info of the user who commented
        user = User.objects.get(pk=int(request.user.id))
        # gets the listing that received the comment
        listing = Listing.objects.get(pk=int(listing_id))
        # creates a comment entry in the database
        commentFile = Comment(listing_name=listing, user_name=user, comment=comment)
        # saves the entry
        commentFile.save()
        return HttpResponseRedirect(reverse("listing_entry", args=(listing_id,)))

@login_required
def wishlist(request, listing_id):
    # gets the user's wishlist
    wishlist = Wishlist.objects.get(user_id=request.user.id)
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
    # gets the current user
    user = request.user
    # gets their wishlist
    wishlist = Wishlist.objects.get(user_id=user.id)
    # gets all the items in their wishlist
    wishlist_items = wishlist.items.all()
    return render(request, "auctions/watchlist.html", {
        "wishlist_items": wishlist_items,
    })

@login_required
def bidding(request, listing_id):
    # current bid
    bid = request.POST["bid"]
    # current listing
    listing = Listing.objects.get(pk=listing_id)
    # tries to get the bid value for the current listing
    try:
        current_bid = Bid.objects.get(listing=listing)
        # if it's higher than the current bid
        if float(bid) > current_bid.bid:
            # gets the user who bade
            current_bid.user = request.user
            # bid value
            current_bid.bid = bid 
            # saves those values
            current_bid.save()
        # if it isn't higher than the current bid
        else:
            message = "ERROR! Bid must be higher than current ammount."
            # returns an error message giving back an error message
            return listing_entry(request, listing_id, message=message)
        # returns the user to the original item's page
        return HttpResponseRedirect(reverse("listing_entry", args=(listing_id,)))
    # if there is no bid on the database
    except Bid.DoesNotExist:
        # checks if the bid price is equal or higher than the bid value and if it's different than 0
        if float(bid) >= listing.price and float(bid) != 0:
            new_bid = Bid(listing=listing, user=request.user, bid=bid)
            # save the user who bade, the bid value and the listing to the database
            new_bid.save()
        # if it doesn't match the if check criteria
        else:
            message = "ERROR! Bid must be higher than current ammount."
            # returns an error message
            return listing_entry(request, listing_id, message=message)
        return HttpResponseRedirect(reverse("listing_entry", args=(listing_id,)))

@login_required
def closeListingWithoutSale(request, listing_id):
    # gets the listing info and then it closes that listing
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    # returns the user a message that they have closes the listing without a sale
    message = "Closed listing without sale"
    return inactive_listing(request, listing_id, message)

@login_required
def close(request, listing_id):
    # gets the listing
    listing = Listing.objects.get(pk=listing_id)
    # gets the comments
    comments = Comment.objects.filter(listing_name=listing)
    # gets the bidding info
    try:
        # tries to get the bidding info
        listing_bid = Bid.objects.get(listing=listing)
    except Bid.DoesNotExist:
        # if there are no bids, then the user has closed the listing without selling the item
        return closeListingWithoutSale(request, listing.id)
    # saves the information of the user who bid, the ammount and which listing
    Winner.objects.create(user=listing_bid.user, listing=listing, sold_by=listing_bid.bid)
    # saves the information to a variable
    inactive_listing_info = Winner.objects.get(listing=listing)
    # makes the listing inactive and saves it
    listing.is_active = False
    listing.save()
    return render(request, "auctions/inactive_listing.html", {
        "listing": listing,
        "comments": comments,
        "winner": inactive_listing_info,
    })

# to show all categories
def categories(request):
    # get all the categories on the database
    categories = Categorie.objects.all()
    return render(request, "auctions/all_categories.html", {
        "categories": categories
    })

# to show items within a categorie
def categorie(request, categorie_id):
    # get the specific categorie clicked
    category = Categorie.objects.get(pk=categorie_id)
    # gets all the listings which co-relate with the categorie chosen
    items = category.listings.all()
    # checks if all items are active
    listings = [item for item in items if item.is_active]
    return render(request, "auctions/category_listings.html", {
        "listings": listings,
        "category": category
    })