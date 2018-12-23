from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
import main.models
from .forms import CommentForm, TagForm, SubForm, PostForm
from .utils import *


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
        query = request.GET.get('search', '')
        if query:
            post_list = main.models.Post.objects.filter(Q(title__icontains=query) |
                                                        Q(content__icontains=query) |
                                                        Q(sub_title__icontains=query))
        else:
            post_list = main.models.Post.objects.all().order_by('publish_date').reverse()
        paginator = Paginator(post_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        return render(request, 'index.html', context={'posts': posts})


class About(View):

    def get(self, request):

        return render(request, 'about.html')


class PostRead(View):
    def get(self, request, slug):
        # if method_get then comment form is empty
        comment_form = CommentForm()
        post, comments = get_post_with_comments(slug)

        return render(request, 'post.html', context={'post': post, 'comments': comments,
                                                     'comment_form': comment_form, 'admin_panel': post})


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = main.models.Post
    template = 'post_create.html'
    model_form = PostForm
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = main.models.Post
    template = 'post_update.html'
    model_form = PostForm
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = main.models.Post
    template = 'post_delete.html'
    redirect_url = 'index'
    raise_exception = True


class TagSelect(ObjectReadMixin, View):
    model = main.models.Tag
    template = 'tag_select.html'


# view for create new tags but you can use admin panel which better
class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = main.models.Tag
    template = 'tag_create.html'
    model_form = TagForm
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = main.models.Tag
    template = 'tag_update.html'
    model_form = TagForm
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = main.models.Tag
    template = 'tag_delete.html'
    redirect_url = 'index'
    raise_exception = True


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
class Comment(View):

    def post(self, request):
        comment_form = CommentForm(request.POST)

        # cleaned_data always contains post
        post_id = comment_form.data['post']
        post = main.models.Post.objects.get(pk=post_id)
        if comment_form.is_valid():
            new_comment = comment_form.save()
            return redirect(post)

        post, comments = get_post_with_comments(post.slug)
        return render(request, 'post.html', context={'post': post, 'comments': comments, 'comment_form': comment_form})
