from django import forms


class LocationHiddenForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput)
    latitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(widget=forms.HiddenInput, max_digits=23, decimal_places=20)
    country = forms.CharField(widget=forms.HiddenInput)

    def to_dict(self):
        return {
            "name": self.data["name"],
            "latitude": self.data["latitude"],
            "longitude": self.data["longitude"],
            "country": self.data["country"]
        }




