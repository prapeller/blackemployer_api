import os
from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        if instance.pk:
            filename = f"{instance.pk}_{instance}.{ext}"
        else:
            filename = "{}.{}".format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


def default_1d_array():
    return []


def default_1d_array_of_strings():
    return ["", ]