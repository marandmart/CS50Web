
from django.shortcuts import render
from django.http import Http404
from random import choice
from django import forms
import markdown2

from django.http import HttpResponse

from . import util

class ContentForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        'class': 'new-entry new-entry-field', 
        'placeholder': "Entry's title",
        }))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        'class': 'new-entry new-entry-field new-entry-textarea',
        'placeholder': "Entry's content",
        'rows': '5',
        'cols': '60',
        }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    try: 
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": markdown2.markdown(util.get_entry(title)),
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
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
        form = ContentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "content": "<h1>Entry already exists</h1><p>Acess or search for it at the homepage.</p>"
                })
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "form": form,
            })
    return render(request, "encyclopedia/new_entry.html", {
        "form": ContentForm(),
    })

def edit(request, title):
    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    form = ContentForm()
    form.fields['title'].initial = title.capitalize()
    form.fields['content'].initial = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

def random(request):
    element = choice(util.list_entries())
    return entry(request, element)