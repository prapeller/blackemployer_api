from django.db import models
from django.contrib.auth import get_user_model


class Tag(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return "{0}_{1}".format(self.pk, self.title)


class Like(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
