from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("wishlist", views.wishlist_page, name="wishlist_page"),
    path("listing/<int:listing_id>", views.listing_entry, name="listing_entry"),
    path("commenting/<int:listing_id>", views.commenting, name="commenting"),
    path("wishlist/<int:listing_id>", views.wishlist, name="wishlist"),
    path("bid/<int:listing_id>", views.bidding, name="bidding"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("inactive_listing/<int:listing_id>", views.inactive_listing, name="inactive_listing"),
    path("categories", views.categories, name="categories"),
    path("categorie/<int:categorie_id>", views.categorie, name="categorie"),
    path("close", views.inactive, name="inactive"),
]
