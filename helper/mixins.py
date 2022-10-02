
class SerializerMixin(object):
    def __init__(self, *args, **kwargs):
        super(SerializerMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].error_messages.get('required'):
                self.fields[field].error_messages['required'] = f'{field} is required.'
            if self.fields[field].error_messages.get('blank'):
                self.fields[field].error_messages['blank'] = f'{field} may not be blank.'
            if self.fields[field].error_messages.get('null'):
                self.fields[field].error_messages['null'] = f'{field} may not be null.'


class ModelUpdateMixin:
    def update(self, **kwargs):
        if self._state.adding:
            raise self.DoesNotExist
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save(update_fields=kwargs.keys())
