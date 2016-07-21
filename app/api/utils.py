from django.core import serializers

def serialize_model(queryset, format='json', fields=None):
    """
    A custom model serializer
    @params:
        - queryset: The queryset to serializer
        - format: The format to serialize the queryset to (JSON, XML)
        - fields: A tuple of field names to return in the data
    """
    return serializers.serialize(format, queryset, fields=fields)
