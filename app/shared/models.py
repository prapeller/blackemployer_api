from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from utils.model_utils import default_1d_array_of_strings


class SeoModel(models.Model):
    seo_title = models.CharField("SEO title", max_length=100, blank=True, null=True)
    seo_description = models.TextField("SEO description", max_length=400, blank=True, null=True)
    seo_keywords = models.CharField("SEO keywords", max_length=200, blank=True, null=True)

    class Meta:
        abstract = True
