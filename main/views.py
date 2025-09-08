from django.shortcuts import render
from .models import Product

def show_main(request):
    context = {
        'app_name': 'Toko Footballer Jago',
        'npm': '2406495546',      # ganti dengan punyamu
        'name': 'Daffa Syafitra',    # ganti dengan namamu
        'class': 'PBP B',        # ganti dengan kelasmu
        'products': Product.objects.all(),  # ambil seluruh produk dari DB
    }
    return render(request, "main.html", context)

