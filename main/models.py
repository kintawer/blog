from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField()
    publish_date = models.DateField(default=timezone.now(), blank=False, null=False)

    def __str__(self):
        return self.title
