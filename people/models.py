from django.db import models
from django.core.urlresolvers import reverse
from localflavor.us.models import USStateField, PhoneNumberField

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from core.util import calc_age, calc_age_dec
from scheduling.models import Contact, Appointment
from study.models import Session, Study

from core.models import BaseModel
from core.fields import LanguageField

PARENT_TYPE = (
    (0, u"Father"),
    (1, u"Mother"),
    (2, u"Guardian"),
    (3, u"Other"),
)

GENDER_TYPE = (
    (0, u"Male"),
    (1, u"Female"),
)

PREFERRED_CONTACT_TYPE = (
    (0, u"Home Phone"),
    (1, u"Mother Email"),
    (2, u"Mother Cell"),
    (3, u"Mother Work"),
    (4, u"Father Email"),
    (5, u"Father Cell"),
    (6, u"Father Work"),
)

ETHNICITY_TYPE = (
    (0, u"Not Hispanic or Latino"),
    (1, u"Hispanic or Latino"),
)

RACE_TYPE = (
    (0, u"White"),
    (1, u"Black or African American"),
    (2, u"American Indian or Alaskan Native"),
    (3, u"Asian"),
    (4, u"Hawaiian Native & Pacific Islander"),
)

HAND_TYPE = (
    (0, u"Right"),
    (1, u"Left"),
    (2, u"Ambidextrous"),
)

FMRI_TYPE = (
    (0, u"Yes"),
    (1, u"No"),
    (2, u"Maybe"),
)

BORN_EARLY_TYPE = (
    (0, u"Yes"),
    (1, u"No"),
)


class Family(BaseModel):
    """
    Model for the family unit. Contains address info for the whole family. Parents
    and children are attached to a family.
    """
    name_text = models.CharField('Name', max_length=100)

    address1 = models.CharField('Address 1', max_length=255, blank=True)
    address2 = models.CharField('Address 2', max_length=255, blank=True)
    city = models.CharField('City', max_length=255, blank=True)
    state = USStateField('State', blank=True)
    zipcode = models.CharField('Zip', max_length=15, blank=True)
    homephone = PhoneNumberField('Home Phone', blank=True)

    preferred_contact_type = models.SmallIntegerField('Preferred Contact', null=True, blank=True, choices=PREFERRED_CONTACT_TYPE)

    notes = models.TextField('Notes', blank=True)

    def __init__(self, *args, **kwargs):
        super(Family, self).__init__(*args, **kwargs)
        self.fontawesome = 'users'

    class Meta:
        verbose_name = 'Family'
        verbose_name_plural = 'Families'
        ordering = ['name_text']

    def __unicode__(self):
        return self.name_text

    def get_absolute_url(self):
        # return reverse('family_detail', args=[str(self.id)])
        return reverse('family_detail', kwargs={'pk': self.id})

    def get_contacts(self):
        """
        Returns all contacts made to the family.
        """
        return Contact.objects.filter(child__in=self.children.all())

    def get_appointments(self):
        """
        Returns all appointments made for the family.
        """
        return Appointment.objects.filter(child__in=self.children.all())

    def _get_parent_count(self):
        """
        Returns the number of parents in the family.
        """
        return Parent.objects.filter(family=self).aggregate(parent_total=models.Count('id'))["parent_total"]
    parent_count = property(_get_parent_count)

    def _get_child_count(self):
        """
        Returns the number of children in the family.
        """
        return Child.objects.filter(family=self).aggregate(child_total=models.Count('id'))["child_total"]
    child_count = property(_get_child_count)


class Parent(BaseModel):
    """
    Model for the parent. Contains basic contact info, and guardian type.
    """
    name_first_text = models.CharField('First Name', max_length=100)
    name_last_text = models.CharField('Last Name', max_length=100)
    guardian_type = models.ForeignKey('Guardian')

    workphone = PhoneNumberField('Work Phone', blank=True)
    cellphone = PhoneNumberField('Cell Phone', blank=True)
    email = models.EmailField(blank=True)

    family = models.ForeignKey('Family', related_name='parents')

    def __init__(self, *args, **kwargs):
        super(Parent, self).__init__(*args, **kwargs)
        self.fontawesome = 'female'

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
        ordering = ['name_last_text', 'name_first_text']

    def __unicode__(self):
        return self.name_last_text + ', ' + self.name_first_text

    def get_absolute_url(self):
        return reverse('parent_detail', kwargs={'pk': self.pk})


class Child(BaseModel):
    """
    Model for the child. Contains multiple ID types.
    """
    babylab_id = models.IntegerField('Baby Lab Subject ID', unique=True, null=True, blank=True)
    kid_neurolab_id = models.IntegerField('Kid Neuro Lab ID', unique=True, null=True, blank=True)

    name_first_text = models.CharField('First Name', max_length=100)
    name_last_text = models.CharField('Last Name', max_length=100)
    gender_type = models.SmallIntegerField('Gender', choices=GENDER_TYPE)
    dob_date = models.DateField('Birth Day')
    ethnicity = models.SmallIntegerField('Ethnicity', choices=ETHNICITY_TYPE, blank=True, null=True)
    race = models.SmallIntegerField('Race', choices=RACE_TYPE, blank=True, null=True)

    handedness = models.SmallIntegerField('Handedness', choices=HAND_TYPE, blank=True, null=True)
    fmri = models.SmallIntegerField('fMRI', choices=FMRI_TYPE, blank=True, null=True)
    fmri_date = models.DateField('fMRI Phone Screened', blank=True, null=True)
    dob_early = models.SmallIntegerField('Born more than 3 weeks early', choices=BORN_EARLY_TYPE, blank=True, null=True)
    disability = models.ManyToManyField('Disability', blank=True, verbose_name='Disability')

    notes = models.TextField('Notes', blank=True)

    family = models.ForeignKey('Family', related_name='children')

    def __init__(self, *args, **kwargs):
        super(Child, self).__init__(*args, **kwargs)
        self.fontawesome = 'child'

    class Meta:
        verbose_name = 'Child'
        verbose_name_plural = 'Children'
        ordering = ['name_last_text', 'name_first_text']

    def __unicode__(self):
        return self.name_last_text + ', ' + self.name_first_text

    def get_absolute_url(self):
        return reverse('child_detail', kwargs={'pk': self.pk})

    def get_null_sessions(self):
        """
        Returns all the sessions the child has NOT attended.
        """
        data = Study.objects.exclude(name_text__in=list(Session.objects.filter(child=self))).values()
        data_dict = [item for item in data]
        for x in data_dict:
            x['child'] = self.id
        return data_dict

    def _get_child_age(self):
        """
        Returns the age of the child, readable format
        """
        if self.dob_date:
            return calc_age(self.dob_date)
        else:
            return None
    age = property(_get_child_age)

    def _get_child_age_dec(self):
        """
        Returns the age of the child, decimal value
        """
        if self.dob_date:
            return calc_age_dec(self.dob_date)
        else:
            return None
    age_dec = property(_get_child_age_dec)

    def _get_lang_eng_heard(self):
        """
        Returns percentage of English heard
        """
        if self.languages.filter(name="en").exists():
            lang = self.languages.get(name="en")
            return lang.percent
            # return "yes"
        else:
            return None
    eng_heard = property(_get_lang_eng_heard)


class Guardian(models.Model):
    """
    Guardian types used by the parent class.
    Meant to be added/edited in the Admin Site.
    """
    name = models.CharField('Name', max_length=100)
    order = models.DecimalField(max_digits=5, decimal_places=2, unique=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Guardian'
        verbose_name_plural = 'Guardians'

    def __unicode__(self):
        return self.name


class Disability(models.Model):
    """
    Disability types used by the child class.
    Meant to be added/edited in the Admin Site.
    """
    name = models.CharField('Name', max_length=100)
    order = models.DecimalField(max_digits=5, decimal_places=2, unique=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Disability'
        verbose_name_plural = 'Disabilities'

    def __unicode__(self):
        return self.name


class Language(models.Model):
    """
    Language(s) spoken in the child class.
    Default language is English, and the percentages should equal 100%.
    """
    name = LanguageField('Name')
    percent = models.SmallIntegerField('Percent',
                                       validators=[
                                           MaxValueValidator(100),
                                           MinValueValidator(0)
                                       ]
                                       )
    child = models.ForeignKey('Child', related_name='languages')

    class Meta:
        ordering = ['name']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __unicode__(self):
        return self.name
