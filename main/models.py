from django.db import models
from froala_editor.fields import FroalaField
from django.db.models import signals
from blog.tasks import send_post_email
from django.shortcuts import reverse
import uuid

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_select', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Post(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=False, null=False, db_index=True)
    sub_title = models.TextField(blank=True, null=True, default='')
    bg_img = models.ImageField(upload_to='bg_posts/', blank=True)
    content = FroalaField()
    publish_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='slug', unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    is_notified = models.BooleanField(auto_created=True, default=False, blank=False)

    def get_absolute_url(self):
        return reverse('post_select', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    unsub_key = models.UUIDField(default=uuid.uuid4, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    # getting dict {'email': , 'unsub_key': }
    def get_email_with_key(self):
        return {'email': self.email, 'unsub_key': str(self.unsub_key)}


# celery def after save post
def post_post_save(sender, instance, signal, *args, **kwargs):
    # Send notification
    if not instance.is_notified:

        instance.is_notified = True
        instance.save()

        sub_list = []
        for sub in Subscribe.objects.filter(is_active=True):
            sub_list.append(sub.get_email_with_key())

        if sub_list:
            send_post_email.delay(sub_list=sub_list, post_title=instance.title, slug=instance.slug)


# signal for send email notification
signals.post_save.connect(post_post_save, sender=Post)


class Comment(models.Model):
    nickname = models.CharField(max_length=30, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.nickname, self.text)


