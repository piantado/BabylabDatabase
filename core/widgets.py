from django import forms
from django.utils.safestring import mark_safe


class CustomDateWidget(forms.DateInput):

    @property
    def media(self):
        js = ('js/bootstrap-datepicker.js', 'js/custom.widget.date.js')
        css = {'all': ('css/datepicker3.css',)}
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'dateinput', 'placeholder': 'YYYY-MM-DD'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(CustomDateWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None):
        input_html = super(CustomDateWidget, self).render(name, value, attrs)
        return mark_safe('<div class="input-group date bootstrap-datepicker"><span class="input-group-addon"><span class="fa fa-calendar"></span></span>%s'
                         '<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>' % (input_html, u'Today'))


class CustomTimeWidget(forms.TimeInput):

    @property
    def media(self):
        js = ('js/bootstrap-timepicker.js', 'js/custom.widget.time.js')
        css = {'all': ('css/bootstrap-timepicker.css',)}
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None, format='%I:%M %p'):
        final_attrs = {'class': 'timeinput', 'placeholder': 'HH:MM AM/PM'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(CustomTimeWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None):
        input_html = super(CustomTimeWidget, self).render(name, value, attrs)
        return mark_safe('<div class="input-group time bootstrap-datepicker"><span class="input-group-addon"><span class="fa fa-clock-o"></span></span>%s'
                         '<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>' % (input_html, u'Now'))


class CustomSplitDateTimeWidget(forms.SplitDateTimeWidget):

    def __init__(self, attrs=None):
        widgets = [CustomDateWidget, CustomTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u'<div class="datetime clearfix">%s%s</div>' %
                        (rendered_widgets[0], rendered_widgets[1]))