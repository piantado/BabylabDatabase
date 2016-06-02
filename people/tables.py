from django_tables2 import tables
from django_tables2.utils import Accessor

from .models import Child, Parent, Family, Language
from core.tables import OpenColumn, BaseTable


class ChildTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Child
        order_by = ('family', 'name_first_text',)
        fields = ('id', 'name_first_text', 'name_last_text', 'family', 'gender_type', 'dob_date', 'age', 'nickname', )

    id = OpenColumn('child_detail', icon='child', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)


class ParentTable(BaseTable):

    class Meta(BaseTable.Meta):
        model = Parent
        fields = ('id', 'name_first_text', 'name_last_text', 'family', 'guardian_type', 'workphone', 'cellphone', 'email', )

    id = OpenColumn('parent_detail', icon='female', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)


class FamilyTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Family
        fields = ('id', 'name_text', 'parents', 'children', 'address1', 'city', 'state', 'zipcode', )

    id = OpenColumn('family_detail', icon='users', kwargs={'pk': Accessor('pk')}, attrs={'a': {'class': 'btn btn-primary btn-sm'}}, verbose_name='Action', orderable=False)
    parents = tables.columns.TemplateColumn(verbose_name='Parents', template_name='people/column_multi_parent.html', orderable=False)
    children = tables.columns.TemplateColumn(verbose_name='Children', template_name='people/column_multi_child.html', orderable=False)


class LanguageTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Language
        order_by = ('name', 'percent',)
        fields = ('name', 'percent', )
        attrs = {"data": "nodatatable"}
