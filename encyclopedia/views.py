from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/404.html", status=404)

    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
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