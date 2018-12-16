from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404
from django.core.paginator import Paginator
import main.models
from .forms import TagForm, CommentForm

# Create your views here.


class Index(View):

    def get(self, request):
        # posts ordered by published date
        post_list = main.models.Post.objects.all().order_by('publish_date').reverse()
        paginator = Paginator(post_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'index.html', context={'posts': posts})


class About(View):

    def get(self, request):

        return render(request, 'about.html')


class Post(View):

    def get(self, request, slug):
        post = get_object_or_404(main.models.Post, slug__iexact=slug)
        comment_form = CommentForm()
        try:
            comments = main.models.Comment.objects.filter(post=post.id).order_by('date').reverse()
        except main.models.Comment.DoesNotExist:
            comments = None

        return render(request, 'post.html', context={'post': post, 'comments': comments,
                                                     'comment_form': comment_form})


class TagCreate(View):

    def get(self, request):
        form = TagForm()
        return render(request, 'tag_create.html', context={'form': form})

    def post(self, request):
        bound_form = TagForm(request.POST)
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return render(request, 'tag_select.html', context={'tag': new_tag})
        return render(request, 'tag_create.html', context={'form': bound_form})


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
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save()
            comment_form = CommentForm()

        post = get_object_or_404(main.models.Post, pk=request.POST.get('post'))
        try:
            comments = main.models.Comment.objects.filter(post=post.id).order_by('date').reverse()
        except main.models.Comment.DoesNotExist:
            comments = None

        return render(request, 'post.html', context={'post': post, 'comments': comments, 'comment_form': comment_form})
