from django_tables2 import tables
from django_tables2.utils import Accessor

from .models import Study, Session

from people.models import Child
from people.models import BORN_EARLY_TYPE
from core.tables import OpenColumn, BaseTable


class StudyTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Study
        order_by = ('name_text',)
        fields = ('id', 'name_text', 'description', 'pi', 'start_date', 'end_date', 'qualifications', )

    id = OpenColumn('study_detail', icon='flask', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)


class SessionListTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Study
        order_by = ('name_text',)
        fields = ('id', 'name_text', 'session_count', 'id2' )

    id = OpenColumn('session_list', icon='clock-o', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Complete', orderable=False)
    id2 = OpenColumn('session_no_list', icon='search', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Search', orderable=False)
    session_count = tables.columns.Column(orderable=False, verbose_name="Completed")


class NoSessionTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Child
        order_by = ('name_last_text', 'name_first_text',)
        # order_by = ('child_fullname',)
        #fields = ('id', 'name_last_text', 'name_first_text', 'gender_type', 'dob_early', 'disability', 'age_dec', 'eng_heard')
        fields = ('id', 'name_last_text', 'name_first_text', 'gender_type', 'dob_early', 'disability', 'age_in_months', 'eng_heard')

    id = OpenColumn('child_detail', icon='child', kwargs={'pk': Accessor('id')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)
    disability = tables.columns.TemplateColumn(attrs={'th': {'class': 'text-search'}}, verbose_name='Disability', template_name='study/column_multi_disability.html', orderable=False)
    dob_early = tables.columns.Column(attrs={'th': {'class': 'filter'}})
    gender_type = tables.columns.Column(attrs={'th': {'class': 'filter'}})



class SessionTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Session
        order_by = ('study',)
        fields = ('id', 'study', 'session_date', 'child', 'dob', 'staff')

    id = OpenColumn('session_detail', icon='clock-o', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)
    dob = tables.columns.DateColumn(accessor='child.dob_date')
