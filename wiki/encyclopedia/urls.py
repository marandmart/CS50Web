from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("<str:title>", views.go_entry, name="go_entry"),
]