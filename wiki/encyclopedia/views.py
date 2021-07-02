from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms    
from markdown2 import Markdown
import re
import random


from . import util
# markdowner = Markdown()
# css = util.get_entry("CSS")

# Create a form class for adding a new entry
class AddEntryForm(forms.Form):
        entryTitle = forms.CharField(label="Title of the entry")
        markdownContent = forms.CharField(label="Content in mark-up language", widget=forms.Textarea())

# Create a form class for editing an entry
class EditEntryForm(forms.Form):
        entryTitle = forms.CharField(label="Title of the entry")
        markdownContent = forms.CharField(label="Content in mark-up language", widget=forms.Textarea())


# Index page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Error page for a missing entry
def error(request, entry):
    return render(request, "encyclopedia/error.html", {
        "error": f"{entry} does not exist in our wiki."
    })

# Wiki entry page
def entry(request, entry):
    wiki = util.get_entry(entry)
    markdowner = Markdown()
    wikiHtml = markdowner.convert(wiki)
    if wiki: 
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "wiki": wikiHtml
        })
    else:
        return error(request, entry)

# Wiki search result page
def search(request):
    # Get the value of the form query: 
    # https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.QueryDict
    q = request.GET.__getitem__("q") # print(q)
    # Get the encyclopedia entry text for the searched item
    searchQuery = util.get_entry(q)
    if searchQuery:
        return render(request, "encyclopedia/entry.html", {
            "entry": q.capitalize(),
            "wiki": searchQuery
        })
    else:
        # Get the full list of encyclopedia entries
        fullEntriesList = util.list_entries()
        # Search for a substring among entries
        r = re.compile(f".*{q}.*", re.IGNORECASE)
        # print(r)
        
        return render(request, "encyclopedia/search.html", {
            "entries": list(filter(r.match, fullEntriesList))
        })

# Add a new entry:
def addEntry(request):

    # Get the list of all current encyclopedia entries
    entries = util.list_entries()

    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = AddEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            newEntryTitle = form.cleaned_data["entryTitle"]
            newMarkdownContent = form.cleaned_data["markdownContent"]
            # Add the new task to our list of tasks
            util.save_entry(newEntryTitle, newMarkdownContent)
            # If the entry already exists, return an error page 
            if newEntryTitle in entries:
                return render(request, "encyclopedia/error.html", {
                    "error": f"{newEntryTitle} already exists in our wiki."
                })
            else:
                # Redirect user to the added entry page
                return render(request, "encyclopedia/entry.html", {
                    "entry": newEntryTitle,
                    "wiki": newMarkdownContent
                })

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/addEntry.html", {
                "form": form
            })

    return render(request, "encyclopedia/addEntry.html", {
        "form": AddEntryForm()
    })



# Edit an entry:
def editEntry(request, entry):

    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = EditEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            entryTitle = form.cleaned_data["entryTitle"]
            newMarkdownContent = form.cleaned_data["markdownContent"]
            if entryTitle == entry:
                # Add the new task to our list of tasks
                util.save_entry(entryTitle, newMarkdownContent)
                # Redirect user to the added entry page
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry,
                    "wiki": newMarkdownContent
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "error": f"You should modify '{entry}' instead of '{entryTitle}'!!!"
                })

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/editEntry.html", {
                "form": form
            })

    if entry not in util.list_entries():
        return render(request, "encyclopedia/error.html", {
                    "error": f"There's no such entry in encyclopedia. Add one yourself by clicking 'Create New Page'! "
                })
    else:
        form = EditEntryForm(initial={"markdownContent": util.get_entry(entry), "entryTitle": entry})

        return render(request, "encyclopedia/editEntry.html", {
            "form": form,
            "entry": entry
        })

# Go to a random entry page
def randomEntry(request):
    currentEntries = util.list_entries()
    randomNumber = random.randrange(0, len(currentEntries))
    print(currentEntries[randomNumber])
    return HttpResponseRedirect(f"http://127.0.0.1:8000/wiki/{currentEntries[randomNumber]}/")
        