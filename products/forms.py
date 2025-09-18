from django import forms
from .models import Comment

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    zip_code = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    telephone = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    shipping_address = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    ship_to_different = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['product','customer','text','stars','is_approved']

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=50, required=True)
