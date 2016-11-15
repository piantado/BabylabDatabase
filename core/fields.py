from django.db.models.fields import CharField
from localflavor.us.models import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

class LanguageField(CharField):
    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        # Local import so the languages aren't loaded unless they are needed.
        from .languages import LANGUAGES

        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', LANGUAGES)
        super(CharField, self).__init__(*args, **kwargs)


# using localflavor.us.models.PhoneNumberField as a 
#template for phone verification (need to ignore no area code typed in)
class RocPhoneNumberField(PhoneNumberField):
    """
    checks that the value is a valid U.S.A.-style phone 
    number (in the format ``XXX-XXX-XXXX`` or 'XXX-XXXX' (585 is automatically added)).
    """
    description = _("Phone number")

    def __init__(self, *args, **kwargs):
        super(RocPhoneNumberField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(RocPhoneNumberField, self).deconstruct()
        #del kwargs['max_length']
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        from .forms import RocUSPhoneNumberField

        defaults = {'form_class': RocUSPhoneNumberField}
        defaults.update(kwargs)
        return super(RocPhoneNumberField, self).formfield(**defaults)