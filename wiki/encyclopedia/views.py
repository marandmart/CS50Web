
from django.shortcuts import render
from django.http import Http404
from django import forms
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def go_entry(request, title):
    try: 
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": markdown2.markdown(util.get_entry(title)),
        })
    except TypeError:
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": "<h1>PAGE DOES NOT EXIST</h1><p>Know the subject? Consider creating an entry for this topic.</p>",
            })

def search_entry(request):
    if request.method == "GET":
        try:
            return render(request, "encyclopedia/entry.html", {
                "title": str(request.GET['q']).capitalize(),
                "content": markdown2.markdown(util.get_entry(str(request.GET['q']))),
            })
        except TypeError:
            return render(request, "encyclopedia/search.html", {
                "entries": util.list_entries(),
                "query": request.GET['q'].lower(),
            })

def new_entry(request):
    if request.method == "POST":
        try:
            title = request.POST['title']
            content = request.POST['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title.capitalize(),
                "content": markdown2.markdown(util.get_entry(title)),
            })
        except PermissionError:
            return render(request, "encyclopedia/entry.html", {
                "title": "ERROR",
                "content": "<h1>Entry already exists. Go to the homepage to look for it.</h1>",
            })
    return render(request, "encyclopedia/new_entry.html")