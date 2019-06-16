from django.db import models
from django.utils.text import slugify
from text_unidecode import unidecode


# Create your models here.
class AbstractTimestamp(models.Model):
    class Meta:
        abstract = True

    create = models.DateTimeField(auto_now_add=True, editable=False)
    update = models.DateTimeField(auto_now=True, editable=False)


class AbstractNamedObj(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=32)


class AbstractUniqueNamedObj(AbstractNamedObj):
    class Meta:
        abstract = True

    name = models.CharField(max_length=32, unique=True)


class AbstractUniqueSlugifyNamedObj(AbstractUniqueNamedObj):
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        #if self.is_new:
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ActivatedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DeactivatedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class AbstractActivated(models.Model):

    class Meta:
        abstract = True

    is_active = models.BooleanField(default=False)
    #objects = models.Manager()
    #activated = ActivatedManager()
    #deactivated = DeactivatedManager()
