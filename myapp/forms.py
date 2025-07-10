from django import forms
from myapp.models import Order

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)

class SearchForm(forms.Form):
    name = forms.CharField(label='Your Name', required=False)
    category = forms.ChoiceField(
        label='Select a category:',
        choices=[
            ('S', 'Science&Tech'),
            ('F', 'Fiction'),
            ('B', 'Biography'),
            ('T', 'Travel'),
            ('O', 'Other')
        ],
        widget=forms.RadioSelect,
        required=False
    )
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': 'Member name'}