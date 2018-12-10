from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.


# class Category(models.Model):
#     category_name = models.CharField(max_length=50, blank=False, null=False)
#
#     def __str__(self):
#         return self.category_name


class Post(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=False, null=False, db_index=True)
    sub_title = models.TextField(blank=True, null=True, default='')
    bg_img = models.ImageField(upload_to='bg_posts/')
    content = FroalaField()
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(default='slug', unique=True)

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Comment(models.Model):
    nickname = models.CharField(max_length=30, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.nickname, self.text)
