from django import forms


class CartAddForm(forms.Form):
    qty = forms.IntegerField(min_value=1, max_value=9)


class CartDetailForm(forms.Form):
    total_amount = forms.FloatField()
    shipping = forms.CharField(max_length=10)
