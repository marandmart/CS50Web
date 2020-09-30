from django.shortcuts import render
from django.http import Http404
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