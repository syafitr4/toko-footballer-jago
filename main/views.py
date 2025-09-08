from django.shortcuts import render
from .models import Product

def show_main(request):
    context = {
        'app_name': 'Football Shop',
        'npm': '240123456',      # ganti dengan punyamu
        'name': 'Haru Urara',    # ganti dengan namamu
        'class': 'PBP A',        # ganti dengan kelasmu
        'products': Product.objects.all(),  # ambil seluruh produk dari DB
    }
    return render(request, "main.html", context)

