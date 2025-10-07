from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
import uuid
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Product


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm': '2406495546',
        'name': request.user.username,
        'class': 'PBP B',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html",context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product': product}
    return render(request, "show_products.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
          user = form.get_user()
          login(request, user)
          response = HttpResponseRedirect(reverse("main:show_main"))
          response.set_cookie('last_login', str(datetime.datetime.now()))
          return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required
def products_json(request):
    """support ?mine=1 untuk filter 'My Products' & kirimkan can_edit flag"""
    mine = request.GET.get('mine') == '1'
    qs = Product.objects.all().order_by('-is_featured', 'name')
    if mine:
        qs = qs.filter(user=request.user)

    uid = request.user.id
    data = [{
        "id": str(p.id),
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "thumbnail": p.thumbnail,
        "category": p.category,
        "is_featured": p.is_featured,
        "can_edit": (p.user_id == uid),   # <- dipakai di UI
    } for p in qs]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def add_product_ajax(request):
    try:
        name = strip_tags(request.POST.get("name", "")).strip()
        price = int(request.POST.get("price", "0"))
        description = strip_tags(request.POST.get("description", "")).strip()
        thumbnail = request.POST.get("thumbnail", "").strip()
        category = request.POST.get("category", "").strip()
        is_featured = (request.POST.get("is_featured") == "on")
        if not name:
            return HttpResponseBadRequest("Name is required")

        Product.objects.create(
            user=request.user,                # <- set pemilik
            name=name, price=price, description=description,
            thumbnail=thumbnail, category=category, is_featured=is_featured
        )
        return HttpResponse(b"CREATED", status=201)
    except Exception as e:
        return HttpResponseBadRequest(str(e).encode())

@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    try:
        # <- hanya pemilik yang boleh
        product = get_object_or_404(Product, pk=uuid.UUID(str(id)), user=request.user)
        product.name = strip_tags(request.POST.get("name", product.name)).strip()
        product.price = int(request.POST.get("price", product.price))
        product.description = strip_tags(request.POST.get("description", product.description)).strip()
        product.thumbnail = request.POST.get("thumbnail", product.thumbnail).strip()
        product.category = request.POST.get("category", product.category).strip()
        product.is_featured = (request.POST.get("is_featured") == "on")
        product.save()
        return HttpResponse(b"UPDATED", status=200)
    except Exception as e:
        return HttpResponseBadRequest(str(e).encode())

@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    # <- hanya pemilik yang boleh
    product = get_object_or_404(Product, pk=uuid.UUID(str(id)), user=request.user)
    product.delete()
    return HttpResponse(b"DELETED", status=200)
