from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import random
import markdown2

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)
class EditEntryForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    html_entry = markdown2.markdown(entry)


    if entry == None:
        return render(request, "encyclopedia/404.html", status=404)

    return render(request, "encyclopedia/entry.html", {
        "entry": html_entry,
        "title": title
    })

def search(request):
    entries = []
    query = request.GET.get('q', '')
    
    for entry in util.list_entries():
        if query == entry:
            return redirect("entry", title=entry)
        if query in entry:
            entries.append(entry)

    return render(request, "encyclopedia/search.html", {
        "entries": entries
    })

def new(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if not form.is_valid():
            return render(request, "encyclopedia/new.html", {"form": form})

        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        for entry in util.list_entries():
            if title == entry:
                messages.error(request, "Error. Page already exists.")
                return render(request, "encyclopedia/new.html", {"form": form})
        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})

def edit(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":

        form = EditEntryForm(request.POST)

        if not form.is_valid():
            return render(request, "encyclopedia/edit.html", {"form": form})

        content = form.cleaned_data["content"]

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditEntryForm(initial={"content": entry})
    })

def random_entry(request):
    entries = util.list_entries()
    
    entry = random.sample(entries, 1)[0]
    
    return redirect("entry", title=entry)