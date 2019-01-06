from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from .forms import CommentForm, TagForm, SubForm, PostForm
from .utils import *


class Index(View):

    def get(self, request):
        # posts ordered by published date
        query = request.GET.get('search', '')
        if query:
            post_list = models.Post.objects.filter(Q(title__icontains=query) |
                                                    Q(content__icontains=query) |
                                                    Q(sub_title__icontains=query))
        else:
            post_list = models.Post.objects.all().order_by('publish_date').reverse()
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

        # increase view count
        ip = get_user_ip(request)
        try:
            viewer = models.Viewer.objects.get(ip=ip, post=post)
        except models.Viewer.DoesNotExist:
            post.viewers += 1
            post.save()
            viewer = models.Viewer(ip=ip, post=post)
            viewer.save()

        return render(request, 'post.html', context={'post': post, 'comments': comments,
                                                     'comment_form': comment_form, 'admin_panel': post})


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = models.Post
    template = 'post_create.html'
    model_form = PostForm
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = models.Post
    template = 'post_update.html'
    model_form = PostForm
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = models.Post
    template = 'post_delete.html'
    redirect_url = 'index'
    raise_exception = True


class TagSelect(ObjectReadMixin, View):
    model = models.Tag
    template = 'tag_select.html'


# view for create new tags but you can use admin panel which better
class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = models.Tag
    template = 'tag_create.html'
    model_form = TagForm
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = models.Tag
    template = 'tag_update.html'
    model_form = TagForm
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = models.Tag
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
        sub = get_object_or_404(models.Subscribe, unsub_key=uuid)
        sub.is_active = False
        sub.save()
        return HttpResponse('Вы ({}) успешно отписались от рассылки уведомлений!'
                            .format(sub.email))


class Comment(View):

    def post(self, request):
        comment_form = CommentForm(request.POST)

        # cleaned_data always contains post
        post_id = comment_form.data['post']
        post = models.Post.objects.get(pk=post_id)
        if comment_form.is_valid():
            new_comment = comment_form.save()
            return redirect(post)

        post, comments = get_post_with_comments(post.slug)
        return render(request, 'post.html', context={'post': post, 'comments': comments, 'comment_form': comment_form})
