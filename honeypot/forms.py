from django import forms

class HoneypotForm(forms.Form):
    honeypot_field = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="Leave this empty",
    )
