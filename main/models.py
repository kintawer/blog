from django.db import models
from froala_editor.fields import FroalaField
from django.db.models import signals
from blog.tasks import send_post_email
from django.http import HttpRequest

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=False, null=False, db_index=True)
    sub_title = models.TextField(blank=True, null=True, default='')
    bg_img = models.ImageField(upload_to='bg_posts/')
    content = FroalaField()
    publish_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='slug', unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


# celery def after save post
def post_post_save(sender, instance, signal, *args, **kwargs):
    # Send verification email
    sub_emails = list(Subscribe.objects.values('email'))
    emails_list = []
    for sub_email in sub_emails:
        emails_list.append(sub_email['email'])
    send_post_email.delay(sub_emails=emails_list, post_title=instance.title, slug=instance.slug)


signals.post_save.connect(post_post_save, sender=Post)


class Comment(models.Model):
    nickname = models.CharField(max_length=30, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.nickname, self.text)


