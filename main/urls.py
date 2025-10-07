from django.urls import path
from .views import create_product, show_product, show_main
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import edit_product
from main.views import delete_product
from .views import (
    products_json, add_product_ajax, update_product_ajax, delete_product_ajax
)
app_name = 'main'

urlpatterns = [
    path("", show_main, name="show_main"),
    path("product/<uuid:id>/", show_product, name="show_product"),
    path("create/", create_product, name="create_product"),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit/', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete/', delete_product, name='delete_product'),
    path("products-json/", products_json, name="products_json"),
    path("product/create-ajax/", add_product_ajax, name="add_product_ajax"),
    path("product/<uuid:id>/update-ajax/", update_product_ajax, name="update_product_ajax"),
    path("product/<uuid:id>/delete-ajax/", delete_product_ajax, name="delete_product_ajax"),


]
