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


#used by both Child and Study, so moved to core (from Child)
class Disability(models.Model):
    """
    Disability types used by the child class.
    Meant to be added/edited in the Admin Site.
    """
    name = models.CharField('Name', max_length=100)
    htmlname = models.CharField('HTML Name', max_length=30) #used as reference for checkbox on session page (11.14.16)
    order = models.DecimalField(max_digits=5, decimal_places=2, unique=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Disability'
        verbose_name_plural = 'Disabilities'

    def __unicode__(self):
        return self.name
