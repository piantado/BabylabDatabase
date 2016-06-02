# from django.utils.dateformat import format
#
# from tastypie import fields
# from tastypie.resources import ModelResource
# from .models import Appointment
#
# from people.models import Child
#
#
# status = {0: 'event-success',
#           1: 'event-info',
#           2: 'event-warning',
#           3: 'event-danger',
#           4: '',
# }
#
#
# class ChildResource(ModelResource):
#     class Meta:
#         queryset = Child.objects.all()
#         resource_name = 'child'
#
#
# class AppointmentResource(ModelResource):
#     child = fields.ForeignKey(ChildResource, 'child')
#
#     class Meta:
#         queryset = Appointment.objects.all()
#         resource_name = 'appointment'
#         collection_name = 'result'
#         fields = ['id']
#         include_resource_uri = False
#
#
#     def dehydrate(self, bundle):
#         # bundle.data['title'] = '<i class="fa fa-child"></i> ' + str(bundle.obj.child) + ' <i class="fa fa-building"></i> ' + str(bundle.obj.room) + ' <i class="fa fa-user-md"></i> ' + str(bundle.obj.run_by) + ' <i class="fa fa-flask"></i> ' + str(bundle.obj.study) + ' <i class="fa fa-calendar"></i> ' + bundle.obj.appointment_datetime.strftime(myformat) + ' - ' + str(bundle.obj.appointment_duration) + ' minutes'
#         bundle.data['title'] = str(bundle.obj.child) + ' ' + str(bundle.obj.room) + ' ' + str(bundle.obj.run_by) + ' ' + str(bundle.obj.study)
#         bundle.data['url'] = '/scheduling/appointment/' + str(bundle.obj.id)
#         bundle.data['class'] = status[bundle.obj.status_type]
#         bundle.data['start'] = int(format(bundle.obj.appointment_datetime, 'U')) * 1000
#         bundle.data['end'] = (int(format(bundle.obj.appointment_datetime, 'U')) + (
#             bundle.obj.appointment_duration * 60)) * 1000
#         del bundle.data['child']
#         return bundle
#
#     def alter_list_data_to_serialize(self, request, data):
#         data['success'] = 1
#         del data['meta']
#         return data