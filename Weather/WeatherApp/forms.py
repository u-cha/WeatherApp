from django import forms


class LocationAddHiddenForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput)
    latitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=7, decimal_places=4)
    longitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=7, decimal_places=4)
    country = forms.CharField(widget=forms.HiddenInput)


class LocationDeleteHiddenForm(forms.Form):
    latitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=7, decimal_places=4)
    longitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=7, decimal_places=4)
