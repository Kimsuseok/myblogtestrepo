from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    read_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', null=True, blank=True) #TODO 카테고리 null false로 하기
    tags = models.ManyToManyField('Tag', null=True, blank=True)
    #files = models.ManyToManyField('Uploadfile', null=True, blank=True)

    def get_absolute_url(self):
        pass

    class Meta:
        ordering = ['-created_date', '-pk']

# TODO depth가 있는 카테고리 구현. 우선은 1단계 카테고리로 구현한다.
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    ordering = models.IntegerField()

class Tag(models.Model):
    name = models.CharField(max_length=100, )

class Uploadfile(models.Model):
    post = models.ForeignKey(Post, default=None)
    file = models.ImageField(upload_to='%Y/%m/%d/', )


