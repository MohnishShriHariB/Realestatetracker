from django import forms
from .models import Favorite

class Searchform(forms.Form):
    search_term=forms.CharField(max_length=255,label="Search for City:")

class latlongform(forms.Form):
    lat=forms.CharField(max_length=255,label="Latitude")
    long=forms.CharField(max_length=255,label="Longitude")

class detailform(forms.ModelForm):
    class Meta:
        model=Favorite
        fields=['type','county','address','price','status','size']
