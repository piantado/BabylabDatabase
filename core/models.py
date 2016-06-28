from django.db import models
from django.utils.safestring import mark_safe
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    title = models.CharField('Staff Title', max_length=50, blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.get_username(), self.get_full_name())


class BaseModel(models.Model):
    """ Base abstract base class to give creation and modified times """
    created = CreationDateTimeField('created')
    modified = ModificationDateTimeField('modified')

    created_by = models.ForeignKey(MyUser, verbose_name='created by', blank=True, null=True, editable=False, related_name="%(app_label)s_%(class)s_created_by")
    modified_by = models.ForeignKey(MyUser, verbose_name='modified by', blank=True, null=True, editable=False, related_name="%(app_label)s_%(class)s_modified_by")

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.fontawesome = 'question'

    def render_fa(self):
        return mark_safe('<span class="fa fa-%s"></span>' % self.fontawesome)


