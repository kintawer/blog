from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from django.core.paginator import Paginator
import main.models

# Create your views here.


class Index(View):

    def get(self, request):
        post_list = main.models.Post.objects.all()
        paginator = Paginator(post_list, 3)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'index.html', context={'posts': posts})


class About(View):

    def get(self, request):

        return render(request, 'about.html')


class Contact(View):

    def get(self, request):

        return render(request, 'contact.html')


class Post(View):

    def get(self, request, slug):
        try:
            post = main.models.Post.objects.get(slug=slug)
        except main.models.Post.DoesNotExist:
            raise Http404("Post does not exist")

        try:
            comments = main.models.Comment.objects.filter(post=post.id).order_by('date')
        except main.models.Comment.DoesNotExist:
            comments = None

        return render(request, 'post.html', context={'post': post, 'comments': comments})


class Subscribe(View):

    def post(self, request):
        email = request.POST.get('subscribe_email')
        sub = main.models.Subscribe.objects.get_or_create(email=email)
        # sub.save()
        return redirect(request.META.get('HTTP_REFERER'))


class Comment(View):

    def post(self, request):
        nickname = request.POST.get('nickname')
        text = request.POST.get('comment')
        post = main.models.Post.objects.get(pk=request.POST.get('post-id'))
        comment = main.models.Comment(nickname=nickname, text=text, post=post)
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
