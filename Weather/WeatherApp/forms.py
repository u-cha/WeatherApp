from django import forms


class LocationAddHiddenForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput)
    latitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    country = forms.CharField(widget=forms.HiddenInput)


class LocationCoordinatesHiddenForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput)
    latitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    country = forms.CharField(widget=forms.HiddenInput)
