from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.http import HttpResponse
import main.models
from .forms import CommentForm, TagForm, SubForm


def get_post_with_comments(slug):
    post = get_object_or_404(main.models.Post, slug__iexact=slug)
    try:
        comments = main.models.Comment.objects.filter(post=post.id).order_by('date').reverse()
    except main.models.Comment.DoesNotExist:
        comments = None

    return post, comments


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
        # if method_get then comment form is empty
        comment_form = CommentForm()
        post, comments = get_post_with_comments(slug)

        return render(request, 'post.html', context={'post': post, 'comments': comments,
                                                     'comment_form': comment_form})

    def post(self, request, slug):
        # if method_post and comment form is valid then empty form, else contains data
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form.save()
            comment_form = CommentForm()

        post, comments = get_post_with_comments(slug)

        return render(request, 'post.html', context={'post': post, 'comments': comments,
                                                     'comment_form': comment_form})


class TagSelect(View):

    def get(self, request, slug):
        tag = get_object_or_404(main.models.Tag, slug__iexact=slug)
        return render(request, 'tag_select.html', context={'tag': tag})


# view for create new tags but you can use admin panel which better
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


class TagUpdate(View):

    def get(self, request, slug):
        tag = get_object_or_404(main.models.Tag, slug__iexact=slug)
        tag_form = TagForm(instance=tag)
        return render(request, 'tag_update.html', context={'tag': tag, 'form': tag_form})

    def post(self, request, slug):
        new_tag = get_object_or_404(main.models.Tag, slug__iexact=slug)
        return redirect(new_tag)


class Subscribe(View):

    def post(self, request):
        email = request.POST.get('subscribe_email')
        sub_form = SubForm({'email': email})

        if sub_form.is_valid():
            sub_form.save()

        return redirect(request.META.get('HTTP_REFERER'))


class UnSubscribe(View):

    def get(self, request, uuid):
        sub = get_object_or_404(main.models.Subscribe, unsub_key=uuid)
        sub.is_active = False
        sub.save()
        return HttpResponse('Вы ({}) успешно отписались от рассылки уведомлений!'
                            .format(sub.email))

# view for create comments but added POST in post view for this
# class Comment(View):
#
#     def post(self, request):
#         comment_form = CommentForm(request.POST)
#
#         if comment_form.is_valid():
#             new_comment = comment_form.save()
#             comment_form = CommentForm()
#
#         post = get_object_or_404(main.models.Post, pk=request.POST.get('post'))
#         try:
#             comments = main.models.Comment.objects.filter(post=post.id).order_by('date').reverse()
#         except main.models.Comment.DoesNotExist:
#             comments = None
#
#         return render(request, 'post.html', context={'post': post, 'comments': comments, 'comment_form': comment_form})
