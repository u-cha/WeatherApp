from django import forms


class LocationHiddenForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput)
    latitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    country = forms.CharField(widget=forms.HiddenInput)


