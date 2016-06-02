from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='title_serialize')
    url = serializers.ReadOnlyField(source='url_serialize')
    class_ = serializers.ReadOnlyField(source='class_serialize')
    start = serializers.ReadOnlyField(source='start_serialize')
    end = serializers.ReadOnlyField(source='end_serialize')

    class Meta:
        model = Appointment
        fields = ('id', 'title', 'url', 'class_', 'start', 'end')

    def __init__(self, *args, **kwargs):
        super(AppointmentSerializer, self).__init__(*args, **kwargs)
        self.fields['class'] = self.fields['class_']
        del self.fields['class_']
