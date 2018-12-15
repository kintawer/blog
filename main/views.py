from django.shortcuts import render, redirect, get_object_or_404
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


class Post(View):

    def get(self, request, slug):
        post = get_object_or_404(main.models.Post, slug__iexact=slug)

        try:
            comments = main.models.Comment.objects.filter(post=post.id).order_by('date')
        except main.models.Comment.DoesNotExist:
            comments = None

        return render(request, 'post.html', context={'post': post, 'comments': comments})


class TagSelect(View):

    def get(self, request, slug):
        tag = get_object_or_404(main.models.Tag, slug__iexact=slug)
        return render(request, 'tag_select.html', context={'tag': tag})


#
class Subscribe(View):

    def post(self, request):
        email = request.POST.get('subscribe_email')
        sub = main.models.Subscribe.objects.get_or_create(email=email)
        # sub.save()
        return redirect(request.META.get('HTTP_REFERER'))


# create comment
class Comment(View):

    def post(self, request):
        nickname = request.POST.get('nickname')
        text = request.POST.get('comment')
        post = main.models.Post.objects.get(pk=request.POST.get('post-id'))
        comment = main.models.Comment(nickname=nickname, text=text, post=post)
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
