from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request: HttpRequest):
    return render(request, 'home.html', context={'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.set_list(list_)
        form.save()
        return redirect(list_)
    else:
        return render(request, 'home.html', context={'form': form})
