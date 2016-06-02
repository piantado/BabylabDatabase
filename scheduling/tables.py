from django_tables2.utils import Accessor

from .models import Appointment, Contact
from core.tables import OpenColumn, BaseTable


class AppointmentTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Appointment
        order_by = ('appointment_datetime', )
        fields = ('id', 'appointment_datetime', 'appointment_duration', 'study', 'room', 'run_by', 'status_type', 'reminder_made_type', 'reminder_datetime', 'confirmation_email_type', 'parking_type', 'babysitter_type', 'notes', 'child', )

    id = OpenColumn('appointment_detail', icon='calendar', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)


class ContactTable(BaseTable):

    class Meta(BaseTable.Meta):
        model = Contact
        order_by = ('contact_datetime', )
        fields = ('id', 'contact_datetime', 'contact_mode_type', 'contact_result_type', 'notes', 'child', )

    id = OpenColumn('contact_detail', icon='phone', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)

