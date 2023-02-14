from django import forms


class CartAddForm(forms.Form):
    qty = forms.IntegerField(min_value=1, max_value=9)