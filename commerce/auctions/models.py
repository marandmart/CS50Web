from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categorie(models.Model):
	category = models.CharField(max_length=64, unique=True)

	def __str__(self):
		return f"{self.id} : {self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_URL = models.URLField(max_length=150, blank=True)
    category = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="listings", default=None)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="itemsOnSale", default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} -> {self.title} costs {self.price}"


class Bid(models.Model):
	user = models.ManyToManyField(User, related_name="bids")
	listing = models.ManyToManyField(Listing, related_name="productBids")
	bid = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.user}, {self.listing} bids {self.bid}"


class Comment(models.Model):
	user = models.ManyToManyField(User, related_name="comments", blank=True)
	listing = models.ManyToManyField(Listing, blank=True)
	comment = models.TextField()

	def __str__(self):
		return f"{self.user}, {self.listing} says {self.comment}"


class Item_categorie(models.Model):
	item_category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="item_category")
	item_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_listing")
	
	def __str__(self):
		return f"{self.item_listing} pertains to {self.item_category}"