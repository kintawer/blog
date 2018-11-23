from django.shortcuts import render, HttpResponse
from django.views import View
import main.models
from django.views.generic import DetailView, ListView

# Create your views here.


class Index(View):

    def get(self, request):
        posts = main.models.Post.objects.all()
        return render(request, 'index.html', context={'posts': posts})


class About(View):

    def get(self, request):

        return render(request, 'about.html')


class Contact(View):

    def get(self, request):

        return render(request, 'contact.html')


class Post(View):

    def get(self, request, slug):
        post = main.models.Post.objects.get(slug=slug)
        return render(request, 'post.html', context={'post': post})


class Subscribe(View):

    def post(self, request):
        email = request.POST.get('subscribe_email')
        sub = main.models.Subscribe.objects.create(email=email)
        sub.save()
        return HttpResponse('Спасибо за подписку')
