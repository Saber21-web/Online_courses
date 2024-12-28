from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(max_length=20)
    exp_month = forms.CharField(max_length=2)
    exp_year = forms.CharField(max_length=4)
    cvc = forms.CharField(max_length=4)
    class Meta:
        model = Payment
        fields = ['course', 'amount']

