from django import forms

class shareTodoForm(forms.Form):
    nameoremail = forms.CharField(label='Name or Email', min_length=3, max_length=100)