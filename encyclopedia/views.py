from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        response = render(request, "encyclopedia/404.html")
        response.status_code = 404
        return response
        
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title
    })