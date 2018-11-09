from django import forms


class Login_form(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)