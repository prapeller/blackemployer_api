import os
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.postgres.fields import ArrayField

from content.models import Like, Tag
from shared.models import SeoModel
from utils.slug import slugify


@deconstructible
class PathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = f'{instance.pk}_{instance}.{ext}'
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


def default_1d_array():
    return []


class Company(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=PathAndRename('images/companies/'),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify("{0}-{1}".format(self.pk, self.title))
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}_{self.title}"


class Comment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(Like, related_name="comment_likes")
    images = ArrayField(models.FileField(upload_to=PathAndRename('images/comments/'),
                                         validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])]),
                        null=True, blank=True, default=default_1d_array
                        )

    def get_likes_quantity(self):
        return sum(self.likes)

    def __str__(self):
        return "{0}_{1}_to_{2}".format(self.pk, self.text[:10], self.company.title)


class Case(SeoModel):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    comments = models.ManyToManyField(Comment, related_name="case_comments")
    tags = models.ManyToManyField(Tag, related_name="case_tags")
    images = ArrayField(models.FileField(upload_to=PathAndRename('images/cases/'),
                                         validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])]),
                        null=True, blank=True, default=default_1d_array
                        )

    def __str__(self):
        return "{0}_{1}_to_{2}".format(self.pk, self.text[:10], self.company.title)
