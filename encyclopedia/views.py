from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import random
import markdown2

from . import util

# Create classes for entry forms
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class' : 'form-control'}))
class EditEntryForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class' : 'form-control'}))

# Render index page with all entries listed
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Render entry page
def entry(request, title):
    entry = util.get_entry(title)
    # Convert markdown to html
    html_entry = markdown2.markdown(entry)

    # Validate if entry exists
    if entry == None:
        return render(request, "encyclopedia/404.html", status=404)

    return render(request, "encyclopedia/entry.html", {
        "entry": html_entry,
        "title": title
    })

# Search for entries
def search(request):
    entries = []
    query = request.GET.get('q', '')
    
    # Check if query matches any in entries list
    # TODO: set entry and all entries to lower case
    for entry in util.list_entries():
        if query == entry:
            # Redirect user to entry page
            return redirect("entry", title=entry)
        if query in entry:
            # Append each query to entries list
            entries.append(entry)

    # Render search results page with a list of all entries that have the query as a substring 
    return render(request, "encyclopedia/search.html", {
        "entries": entries
    })

# Create a new entry
def new(request):
    if request.method == "POST":
        # Create a new entry form, which includes a title and content
        form = NewEntryForm(request.POST)

        # Validate form
        if not form.is_valid():
            # If not valid, render new entry page along with form data submitted by user
            return render(request, "encyclopedia/new.html", {"form": form})

        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        # Check if entry already exists with the provided title
        for entry in util.list_entries():
            if title == entry:
                messages.error(request, "Error. Page already exists.")
                return render(request, "encyclopedia/new.html", {"form": form})
        # Save entry to disk and redirect to new entry's page
        util.save_entry(title, content)
        return redirect("entry", title=title)

    # Render new entry form page
    return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})

# Edit existing entry's markdown content
def edit(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":

        # Create an edit entry form, which includes only content
        form = EditEntryForm(request.POST)

        # Validate form
        if not form.is_valid():
            # If not valid, render edit entry page along with form data submitted by user
            return render(request, "encyclopedia/edit.html", {"form": form})

        content = form.cleaned_data["content"]

        # Save edited entry to disk and redirect to edited entry's page
        util.save_entry(title, content)
        return redirect("entry", title=title)

    # Render edit entry form page with existing content pre-populated
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditEntryForm(initial={"content": entry})
    })

# Take user to a random entry
def random_entry(request):
    entries = util.list_entries()
    
    entry = random.sample(entries, 1)[0]
    
    return redirect("entry", title=entry)