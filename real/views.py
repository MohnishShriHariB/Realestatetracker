from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.forms.utils import ErrorList
from django.http import Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Searchform,latlongform,detailform
from .models import Favorite
import urllib
import requests
import random

LATLONG_API_KEY="your API_kEY for Geocode API"
# Create your views here.
def home(request):
    return render(request,'real\home.html')

@login_required
def dashboard(request):
    favorites=Favorite.objects.filter(user=request.user)
    return render(request,"real\dashboard.html",{'favorites':favorites})

class delete(LoginRequiredMixin,generic.DeleteView):
    model=Favorite
    template_name="real/delete.html"
    success_url=reverse_lazy("dashboard")

    def get_object(self):
        place=super(delete,self).get_object()
        if not place.user == self.request.user:
            raise Http404
        else:
            return place

@login_required
def search(request):
    latlong_form=latlongform()
    search_form=Searchform()
    detail_form=detailform()
    if request.method=="POST":
        form=detailform(request.POST)
        if form.is_valid():
            detail=Favorite()
            detail.type=form.cleaned_data.get("type")
            detail.county=form.cleaned_data.get("county")
            detail.address=form.cleaned_data.get("address")
            detail.price=form.cleaned_data.get("price")
            detail.status=form.cleaned_data.get("status")
            detail.user=request.user
            detail.save()
            return redirect("home")
    return render(request,"real\search.html",{"search_form":search_form,'latlongform':latlong_form,'detailform':detail_form})

def searcharea(request):
    search_form=Searchform(request.GET)
    if search_form.is_valid():
        encoded_search_text=urllib.parse.quote(search_form.cleaned_data['search_term'])
        response=requests.get(f'https://api.geoapify.com/v1/geocode/search?text={ encoded_search_text }&lang=en&limit=6&type=city&apiKey={ LATLONG_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({'result':'no results found'})

def placesearch(request):
    latlong_form=latlongform(request.GET)
    if latlong_form.is_valid():
        lat = urllib.parse.quote(latlong_form.cleaned_data['lat'])
        long = urllib.parse.quote(latlong_form.cleaned_data['long'])
        url = "https://realty-mole-property-api.p.rapidapi.com/properties"

        querystring = {"latitude":str(lat),"longitude":str(long),"limit":"10"}

        headers = "Your API_kEY for Reality Mole Property API"
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
        return JsonResponse(response.json(), safe=False)
    return JsonResponse({'result':'no results found'})

class Signup(generic.CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('dashboard')
    template_name="registration/signup.html"

    def form_valid(self,form):
        view=super(Signup,self).form_valid(form)
        username,password=form.cleaned_data.get("username"),form.cleaned_data.get("password1")
        user=authenticate(username=username,password=password)
        login(self.request,user)
        return view
