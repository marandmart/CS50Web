from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("random", views.random, name="random"),
    path("search_entry", views.search_entry, name="search_entry"),
]