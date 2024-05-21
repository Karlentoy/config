from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    city = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)