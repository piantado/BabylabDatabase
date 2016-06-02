from django.utils.safestring import mark_safe

from django_tables2 import tables
from django_tables2.utils import AttributeDict


class BaseTable(tables.Table):
    class Meta:
        orderable = False
        paginate = False
        default = ''


class OpenColumn(tables.columns.LinkColumn):
    def __init__(self, viewname, urlconf=None, args=None, kwargs=None, current_app=None, attrs=None, icon=None, **extra):
        super(OpenColumn, self).__init__(viewname, urlconf, args, kwargs, current_app, attrs, **extra)
        self.icon = icon

    def render_link(self, uri, text, attrs=None):
        super(OpenColumn, self).render_link(uri, text, attrs)
        attrs = AttributeDict(attrs if attrs is not None else
                              self.attrs.get('a', {}))
        attrs['href'] = uri
        html = '<a {attrs}><span class="fa fa-{icon}"></span> {text}</a>'.format(
            attrs=attrs.as_html(),
            icon=self.icon,
            text='Open'
        )
        return mark_safe(html)

