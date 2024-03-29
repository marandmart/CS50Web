from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categorie(models.Model):
	category = models.CharField(max_length=64, unique=True)

	def __str__(self):
		return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_URL = models.URLField(max_length=150, blank=True)
    category = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="listings", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="itemsOnSale", default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} costs {self.price}"

class Wishlist(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_list", default=None, unique=True)
	items = models.ManyToManyField(Listing, related_name="list_item")

	def __str__(self):
		return f"{self.user} wants {self.items.all()}"

class Bid(models.Model):
	listing = models.OneToOneField(Listing, related_name="productBids", on_delete=models.CASCADE, default=None, blank=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider", blank=True, null=True)
	bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f"{self.user}, {self.listing} bids {self.bid}"


class Comment(models.Model):
	listing_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="onSale", default=None)
	user_name = models.ForeignKey(User, on_delete=models.PROTECT, related_name="commenter", default=None)
	comment = models.TextField()

	def __str__(self):
		return f"{self.user_name}, on {self.listing_name} says {self.comment}"

class Winner(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	listing = models.OneToOneField(Listing, on_delete=models.PROTECT)
	sold_by = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)

	def __str__(self):
		return f"{self.user} won the auction: {self.listing}"