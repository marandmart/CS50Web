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
]
