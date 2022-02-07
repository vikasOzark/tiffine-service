from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='menu.html')

class OrderPlace(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='deatail_view.html')