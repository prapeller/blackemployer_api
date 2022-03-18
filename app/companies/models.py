from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.db import models

from shared.models import SeoModel
from content.models import Tag, Like
from utils.model_utils import PathAndRename, default_1d_array, default_1d_array_of_strings
from utils.slug import slugify


class Company(SeoModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    website = models.URLField(max_length=128, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=PathAndRename("images/companies/"),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(["svg", "jpg", "jpeg", "png"])])

    def save(self, *args, **kwargs):
        self.slug = slugify("{0}-{1}".format(self.pk, self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class Contact(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    phones = ArrayField(models.CharField(max_length=128, null=True, blank=True), default=default_1d_array_of_strings)
    emails = ArrayField(models.CharField(max_length=128, null=True, blank=True), default=default_1d_array_of_strings)
    telegram = models.CharField(max_length=128, null=True, blank=True)
    skype = models.CharField(max_length=128, null=True, blank=True)
    slack = models.CharField(max_length=128, null=True, blank=True)
    other = models.CharField(max_length=128, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class Case(SeoModel):
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    contacts = models.ManyToManyField(Contact, related_name="case_contacts")
    case_date = models.DateTimeField(blank=True, null=True)
    case_description = models.TextField(null=True, blank=True)
    position = models.CharField(max_length=256, blank=True, null=True)
    position_description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="case_tags")
    images = ArrayField(models.FileField(upload_to=PathAndRename("images/cases/"),
                                         validators=[FileExtensionValidator(["svg", "jpg", "jpeg", "png"])]),
                        null=True, blank=True, default=default_1d_array
                        )

    def save(self, *args, **kwargs):
        self.slug = slugify("{0}-{1}".format(self.pk, self.position))
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.slug}"


class Comment(SeoModel):
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, default=None)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(Like, related_name="comment_likes")
    images = ArrayField(models.FileField(upload_to=PathAndRename("images/comments/"),
                                         validators=[FileExtensionValidator(["svg", "jpg", "jpeg", "png"])]),
                        null=True, blank=True, default=default_1d_array
                        )

    # def save(self, *args, **kwargs):
    #     self.slug = slugify("{0}-comment-{1}".format(self.pk, self.case))
    #     super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def get_likes_quantity(self):
        return sum(self.likes)

    def __str__(self):
        return "{0}-comment-{1}".format(self.pk, self.case)
