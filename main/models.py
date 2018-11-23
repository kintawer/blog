from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=False, null=False, db_index=True)
    content = models.TextField(blank=True, db_index=True)
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.title
