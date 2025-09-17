from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    # tambahkan placeholder kosong di paling atas
    category = forms.ChoiceField(
        choices=[('', '— pilih kategori —')] + list(Product.Category.choices),
        required=True
    )

    class Meta:
        model = Product
        fields = ["name", "price", "description", "category", "thumbnail", "is_featured"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
        }
