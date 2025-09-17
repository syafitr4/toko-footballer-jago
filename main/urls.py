from django.urls import path
from .views import create_product, show_product, show_main

app_name = 'main'

urlpatterns = [
    path("", show_main, name="show_main"),
    path("product/<uuid:id>/", show_product, name="show_product"),
    path("create/", create_product, name="create_product"),

]
