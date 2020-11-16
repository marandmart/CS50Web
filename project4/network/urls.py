
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:page_number>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),

    path("user/<int:user_id>", views.profile, name="profile"),
    path("user/<int:user_id>/page/<int:page_number>", views.profile, name="profile"),

    path("user/following", views.following, name="following"),
    path("user/following/page/<int:page_number>", views.following, name="following"),

    # API
    path("user/follow_unfollow/<int:user_id>", views.follow_unfollow, name="follow_unfollow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    # API URLs for the following, index and profile pages
    path("user/like_dislike/<int:post_id>", views.like_dislike, name="like_dislike"),
    path("like_dislike/<int:post_id>", views.like_dislike, name="like_dislike"),
]
