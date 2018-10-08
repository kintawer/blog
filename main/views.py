from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

# Create your views here.


class Index(View):

    def get(self, request):

        return render(request, 'index.html')


class About(View):

    def get(self, request):

        return render(request, 'about.html')


class Contact(View):

    def get(self, request):

        return render(request, 'contact.html')


class Post(View):

    def get(self, request):

        return render(request, 'post.html')