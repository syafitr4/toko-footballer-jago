# main/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import (
    HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import datetime
import uuid

from .forms import ProductForm
from .models import Product

# ========================= PAGES =========================

@login_required(login_url='main:login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        "npm": "2406495546",
        "name": request.user.username,
        "class": "PBP B",
        "product_list": product_list,
        "last_login": request.COOKIES.get("last_login", "Never"),
    }
    return render(request, "main.html", context)

@login_required(login_url='main:login')
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect("main:show_main")
    return render(request, "create_product.html", {"form": form})

@login_required(login_url='main:login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "show_products.html", {"product": product})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect("main:login")
    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            resp = HttpResponseRedirect(reverse("main:show_main"))
            resp.set_cookie("last_login", str(datetime.datetime.now()))
            return resp
    else:
        form = AuthenticationForm(request)
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    resp = HttpResponseRedirect(reverse("main:login"))
    resp.delete_cookie("last_login")
    return resp

@login_required(login_url='main:login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_main")
    return render(request, "edit_product.html", {"form": form})

@login_required(login_url='main:login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse("main:show_main"))

# ========================= DATA / API =========================

@login_required(login_url='main:login')
def products_json(request):
    """Support ?mine=1 untuk filter 'My Products' & kirim can_edit flag"""
    mine = request.GET.get("mine") == "1"
    qs = Product.objects.all().order_by("-is_featured", "name")
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
        "can_edit": (p.user_id == uid),
    } for p in qs]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def add_product_ajax(request):
    try:
        name = strip_tags(request.POST.get("name", "")).strip()
        price = int(request.POST.get("price", "0"))
        description = strip_tags(request.POST.get("description", "")).strip()
        thumbnail = (request.POST.get("thumbnail") or "").strip()
        category = (request.POST.get("category") or "").strip()
        is_featured = (request.POST.get("is_featured") == "on")

        if not name:
            return HttpResponseBadRequest("Name is required")

        Product.objects.create(
            user=request.user,
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
        product = get_object_or_404(Product, pk=uuid.UUID(str(id)), user=request.user)
        product.name = strip_tags(request.POST.get("name", product.name)).strip()
        product.price = int(request.POST.get("price", product.price))
        product.description = strip_tags(request.POST.get("description", product.description)).strip()
        product.thumbnail = (request.POST.get("thumbnail", product.thumbnail) or "").strip()
        product.category = (request.POST.get("category", product.category) or "").strip()
        product.is_featured = (request.POST.get("is_featured") == "on")
        product.save()
        return HttpResponse(b"UPDATED", status=200)
    except Exception as e:
        return HttpResponseBadRequest(str(e).encode())

@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=uuid.UUID(str(id)), user=request.user)
    product.delete()
    return HttpResponse(b"DELETED", status=200)

# ========================= AUTH (AJAX) =========================

User = get_user_model()

def _auth_ok(user):
    return JsonResponse({"ok": True, "username": user.username})

@csrf_exempt
@require_POST
def login_ajax(request):
    username = (request.POST.get("username") or "").strip()
    password = request.POST.get("password") or ""
    try:
        u = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid username or password")
    user = authenticate(request, username=u.username, password=password)
    if user is None:
        return HttpResponseBadRequest("Invalid username or password")
    login(request, user)
    return _auth_ok(user)

@csrf_exempt
@require_POST
def register_ajax(request):
    username = (request.POST.get("username") or "").strip()
    password1 = request.POST.get("password1") or ""
    password2 = request.POST.get("password2") or ""

    if not username or not password1:
        return HttpResponseBadRequest("Username & password are required")
    if User.objects.filter(username__iexact=username).exists():
        return HttpResponseBadRequest("Username already exists")
    if password1 != password2:
        return HttpResponseBadRequest("Passwords do not match")
    if len(password1) < 6:
        return HttpResponseBadRequest("Password must be at least 6 characters")

    user = User.objects.create_user(username=username.lower(), password=password1)
    login(request, user)
    return _auth_ok(user)

@csrf_exempt
@require_POST
def logout_ajax(request):
    logout(request)
    return HttpResponse(b"LOGGED_OUT", status=200)

# ======= FRAGMENT (untuk tombol Refresh & auto-refresh CRUD) =======

@login_required(login_url='main:login')
def products_fragment(request):
    products = Product.objects.filter(user=request.user).order_by("-id")
    html = render_to_string("partials/product_cards.html", {"products": products}, request)
    return JsonResponse({"html": html})
