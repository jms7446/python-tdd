from django.shortcuts import render, redirect
from django.http import HttpRequest
from lists.models import Item


def home_page(request: HttpRequest):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        return redirect('/')

    return render(request, 'home.html', {'items': Item.objects.all()})
