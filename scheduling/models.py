from django.db import models
from django.core.urlresolvers import reverse

from core.models import BaseModel

from django.utils.dateformat import format


CONTACT_MODE_TYPE = (
    (0, u"Home Phone"),
    (1, u"Mother's Cell"),
    (2, u"Mother's Work"),
    (3, u"Father's Cell"),
    (4, u"Father's Work"),
    (5, u"Email"),
    (6, u"Parent called us"),
)

CONTACT_RESULT_TYPE = (
    (0, u"Appt Made"),
    (1, u"Appt Declined"),
    (2, u"Call Again Later"),
    (3, u"Left Message"),
    (4, u"No Contact Made"),
    (5, u"Cancelled Appt"),
    (6, u"Does Not Qualify"),
    (7, u"Entered Into Database"),
)

REMINDER_MADE_TYPE = (
    (0, u"No"),
    (1, u"Parent"),
    (2, u"Message"),
)

APPOINTMENT_STATUS_TYPE = (
    (0, u"Completed"),
    (1, u"Rescheduled"),
    (2, u"No Show"),
    (3, u"Cancelled"),
    (4, u"Scheduled"),
    (5, u"Tentative"),
)

YES_NO_TYPE = (
    (0, u"Yes"),
    (1, u"No"),
)

YES_NO_MAYBE_TYPE = (
    (0, u"Yes"),
    (1, u"No"),
    (2, u"Maybe"),
)


class Contact(BaseModel):
    contact_datetime = models.DateTimeField('Contact Date/Time')
    contact_mode_type = models.SmallIntegerField('Mode of Contact', choices=CONTACT_MODE_TYPE)
    contact_result_type = models.SmallIntegerField('Result', choices=CONTACT_RESULT_TYPE)
    notes = models.TextField('Notes', blank=True)

    staff = models.ForeignKey('core.MyUser', models.CASCADE)

    child = models.ForeignKey('people.Child', models.CASCADE, related_name='contacts')

    # study = models.ManyToManyField('study.Study', blank=True, verbose_name='studys Discussed')

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.fontawesome = 'phone'

    def __unicode__(self):
        return unicode(self.contact_datetime)

    def get_absolute_url(self):
        return reverse('child_detail', kwargs={'pk': self.child_id})

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['contact_datetime']


class Appointment(BaseModel):
    appointment_datetime = models.DateTimeField('Appointment Date/Time')
    appointment_duration = models.IntegerField('Duration', help_text='(Minutes)')
    study = models.ForeignKey('study.Study', models.CASCADE, verbose_name='Study')
    room = models.ForeignKey('Room', models.CASCADE, verbose_name='Room', blank=True, null=True)
    run_by = models.ForeignKey('core.MyUser', models.CASCADE, verbose_name='Run By', blank=True, null=True)
    status_type = models.SmallIntegerField('Status', choices=APPOINTMENT_STATUS_TYPE)

    reminder_made_type = models.SmallIntegerField('Reminder Made', choices=REMINDER_MADE_TYPE, blank=True, null=True)
    reminder_datetime = models.DateTimeField('Reminder Date/Time', blank=True, null=True)
    confirmation_email_type = models.SmallIntegerField('Confirmation Email', choices=YES_NO_TYPE, blank=True, null=True)

    parking_type = models.SmallIntegerField('Parking', choices=YES_NO_MAYBE_TYPE, blank=True, null=True)
    parking_note = models.CharField('Parking Note', max_length=255, blank=True)
    babysitter_type = models.SmallIntegerField('Babysitter', choices=YES_NO_TYPE, blank=True, null=True)

    notes = models.TextField('Notes', blank=True)

    child = models.ForeignKey('people.Child', models.CASCADE, related_name='appointments')

    # TODO:  Show Siblings
    # TODO:  Show child Age at time of appointment

    def __init__(self, *args, **kwargs):
        super(Appointment, self).__init__(*args, **kwargs)
        self.fontawesome = 'calendar'

    def __unicode__(self):
        return unicode(self.appointment_datetime)

    def get_absolute_url(self):
        return reverse('child_detail', kwargs={'pk': self.child_id})

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['appointment_datetime']

    def title_serialize(self):
        #return self.child.name_first_text + ' ' + self.child.name_last_text + ' ' + ' ' + self.room.name + ' ' + self.run_by.username + ' ' + self.study.name_text
        return self.child.name_first_text + ' ' + self.child.name_last_text + ' ' + self.study.name_text

    def url_serialize(self):
        return reverse('appointment_detail', kwargs={'pk': self.id})

    def class_serialize(self):
        status = {0: 'event-success',
          1: 'event-info',
          2: 'event-warning',
          3: 'event-important',
          4: '',
          5: 'event-inverse',
                  }
        return status[self.status_type]

    def start_serialize(self):
        return int(format(self.appointment_datetime, 'U')) * 1000

    def end_serialize(self):
        return (int(format(self.appointment_datetime, 'U')) + (self.appointment_duration * 60)) * 1000


class Room(models.Model):
    name = models.CharField('Room Name', max_length=255)

    def __unicode__(self):
        return self.name
    #
    # def get_absolute_url(self):
    #     return reverse('child_detail', kwargs={'pk': self.child_id})

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['name']