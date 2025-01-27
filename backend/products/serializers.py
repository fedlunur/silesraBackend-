from rest_framework import serializers
from django.apps import apps

def create_serializer_for_model(model):


    class DynamicSerializer(serializers.ModelSerializer):
        class Meta:
            model = model
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Dynamically include nested serializers for foreign keys
            for field_name, field in self.fields.items():
                if isinstance(field, serializers.PrimaryKeyRelatedField):
                    related_model = field.queryset.model
                    # Recursively generate a nested serializer for the related model
                    field.queryset = related_model.objects.all()
                    self.fields[field_name] = create_serializer_for_model(related_model)()

    return DynamicSerializer

def get_serializer_for_model_name(model_name):
    """
    Get a serializer class for a given model name.
    """
    try:
        model = apps.get_model(model_name)
        return create_serializer_for_model(model)
    except LookupError:
        raise Exception(f"Model '{model_name}' not found.")

# Example usage:
# serializer_class = get_serializer_for_model_name('your_app.Organization')