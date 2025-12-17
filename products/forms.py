from django import forms
from .models import Product,Order,Cart,CartItem
input_css_class = "mt-1 block rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 border-slate-400"

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ["name","handle","price","image_url","stock"]
  def __init__(self, *args, **kwargs):
    super().__init__(*args,**kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = input_css_class
class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ["cart_id","total"]