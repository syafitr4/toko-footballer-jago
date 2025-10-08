# main/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # ===== Pages =====
    path("", views.show_main, name="show_main"),
    path("product/<uuid:id>/", views.show_product, name="show_product"),
    path("create/", views.create_product, name="create_product"),
    path("product/<uuid:id>/edit/", views.edit_product, name="edit_product"),
    path("product/<uuid:id>/delete/", views.delete_product, name="delete_product"),

    # ===== Data/API (AJAX) =====
    path("products-json/", views.products_json, name="products_json"),
    path("products/fragment/", views.products_fragment, name="products_fragment"),
    path("product/create-ajax/", views.add_product_ajax, name="add_product_ajax"),
    path("product/<uuid:id>/update-ajax/", views.update_product_ajax, name="update_product_ajax"),
    path("product/<uuid:id>/delete-ajax/", views.delete_product_ajax, name="delete_product_ajax"),

    # ===== Auth (form & AJAX) =====
    path("auth/register/", views.register, name="register"),
    path("auth/login/", views.login_user, name="login"),
    path("auth/logout/", views.logout_user, name="logout"),
    path("auth/register-ajax/", views.register_ajax, name="register_ajax"),
    path("auth/login-ajax/", views.login_ajax, name="login_ajax"),
    path("auth/logout-ajax/", views.logout_ajax, name="logout_ajax"),
]
