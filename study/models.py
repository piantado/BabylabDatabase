from django.db import models
from django.core.urlresolvers import reverse

from core.models import BaseModel


class Study(BaseModel):
    name_text = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    age_min = models.DecimalField('Age (Minimum)', max_digits=5, decimal_places=2, null=True, blank=True)
    age_max = models.DecimalField('Age (Maximum)', max_digits=5, decimal_places=2, null=True, blank=True)
    percent_english_heard = models.SmallIntegerField('Percent English Heard', null=True, blank=True)
    hearing_vision_impaired = models.BooleanField('Hearing/Vision Impaired', default=False)
    born_early = models.BooleanField('Born Early', default=False)
    qualifications = models.TextField('Qualifications', blank=True)

    pi = models.ForeignKey('core.MyUser', verbose_name='PI')

    def __init__(self, *args, **kwargs):
        super(Study, self).__init__(*args, **kwargs)
        self.fontawesome = 'flask'

    def __unicode__(self):
        return self.name_text

    def session_count(self):
        return Session.objects.filter(study=self).aggregate(session_total=models.Count('id'))["session_total"]

    session_count.short_description = 'Session Count'

    def session_no_count(self):
        from people.models import Child
        return Child.objects.all().aggregate(child_total=models.Count('id'))["child_total"] - self.session_count()
        # return Child.objects.all().aggregate() - self.session_count()

    session_no_count.short_description = 'No Session Count'

    def session_taken(self):
        return Session.objects.filter(study=self)

    def session_not_taken(self):
        from people.models import Child
        children = Session.objects.filter(study=self).values_list('child', flat=True)
        children_ids = children
        data = Child.objects.exclude(id__in=list(children_ids))
        return data

    def id2(self):
        return self.id

    # def get_absolute_url(self):
    #     return reverse('family_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'
        ordering = ['name_text']


class Session(BaseModel):
    study = models.ForeignKey('Study', related_name='sessions', verbose_name='Study')
    session_date = models.DateField('Session Date')
    staff = models.ForeignKey('core.MyUser', verbose_name='Staff')

    child = models.ForeignKey('people.Child', related_name='sessions', verbose_name='Child', null=True)

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.fontawesome = 'clock-o'

    def __unicode__(self):
        return unicode(self.study)

    def get_absolute_url(self):
        return reverse('child_detail', kwargs={'pk': self.child_id})

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        unique_together = ('study', 'child')

