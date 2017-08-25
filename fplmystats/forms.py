from django import forms


class InputForm(forms.Form):
    field = forms.IntegerField(None, 0)
