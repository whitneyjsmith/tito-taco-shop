from django import forms
from .models import ProductAttributeStock


class ProductSizeForm(forms.Form):
    size = forms.ModelChoiceField(queryset=ProductAttributeStock.objects.all())

    def __init__(self, *args, **kwargs):
        super(ProductSizeForm, self).__init__(*args, **kwargs)
        self.fields['size'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.attribute.value
