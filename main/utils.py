from . import models
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404


class ObjectCreateMixin(View):
    model = None
    template = None
    model_form = None

    def get(self, request):
        return render(request, self.template, context={'form': self.model_form})

    def post(self, request):
        bound_form = self.model_form(request.POST, request.FILES)
        if bound_form.is_valid():
            obj = bound_form.save()
            return redirect(obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectReadMixin(View):
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'admin_panel': obj})


class ObjectUpdateMixin(View):
    model = None
    template = None
    model_form = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj, 'form': bound_form})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        bound_form = self.model_form(request.POST, request.FILES, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'form': bound_form})


class ObjectDeleteMixin(View):
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        obj.delete()
        return redirect(self.redirect_url)


def get_post_with_comments(slug):
    post = get_object_or_404(models.Post, slug__iexact=slug)
    try:
        comments = models.Comment.objects.filter(post=post.id).order_by('date').reverse()
    except models.Comment.DoesNotExist:
        comments = None

    return post, comments


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
