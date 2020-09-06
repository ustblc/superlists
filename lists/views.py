from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request: HttpRequest):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_.get_get_absolute_url())

    return render(request, "list.html", {"list": list_, "form": form})


def new_list(request: HttpRequest):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_.get_get_absolute_url())
    else:
        return render(request, "home.html", {"form": form})
