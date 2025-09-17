from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def show_main(request):
    product_list = Product.objects.all()
    context = {
        'npm': '2406495546',     # isi punyamu
        'name': 'Daffa Syafitra',     # isi punyamu
        'class': 'PBP B',        # isi punyamu
        'product_list': product_list,
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product': product}
    return render(request, "show_products.html", context)
