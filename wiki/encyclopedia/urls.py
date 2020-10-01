from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("search_entry", views.search_entry, name="search_entry"),
    path("<str:title>", views.go_entry, name="go_entry"),
]