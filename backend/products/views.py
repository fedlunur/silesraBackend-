from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import *
from products.models import *
from backend.utils import *
from datetime import datetime, time
from django.utils import timezone
from django.http import JsonResponse
# Generic Serializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Q
import json
import traceback

class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        model_name = kwargs.pop('model_name', None)
        super().__init__(*args, **kwargs)

        if model_name:
            self.Meta.model = model_mapping.get(model_name)

        if model_name in donot_include_fields:
            for field in donot_include_fields[model_name]:
                self.fields.pop(field, None)

        # Handle ForeignKey fields
        for field in self.Meta.model._meta.get_fields():
            if field.is_relation and field.many_to_one:
                self.fields[field.name] = self.RelationField(field.related_model)

    class RelationField(serializers.PrimaryKeyRelatedField):
        """ Custom field to handle both ID-based writes and detailed reads. """
        def __init__(self, model, **kwargs):
            self.model = model
            super().__init__(queryset=model.objects.all(), **kwargs)

        def to_representation(self, value):
            """ Convert to { "id": value.id, "name": value.name } for GET requests. """
            if isinstance(value, serializers.PKOnlyObject):  
                # Fetch full instance when DRF optimizes the queryset
                value = self.get_queryset().get(pk=value.pk)  
            return {"id": value.id, "name": getattr(value, "name", str(value))}

        def to_internal_value(self, data):
            """ Convert ID to object for POST/PUT requests. """
            return self.get_queryset().get(pk=data)




class GenericModelViewSet(viewsets.ModelViewSet):
  
    def get_queryset(self):
        model_name = self.basename if self.basename.islower() else self.basename.lower()
         
        model = model_mapping.get(model_name)
        
        if model is None:
            raise AssertionError(f"Model not found for basename '{model_name}'")

        return model.objects.all()

    def get_serializer_class(self):
        return DynamicFieldSerializer
        


    def get_serializer(self, *args, **kwargs):
        # Pass the model name to the serializer's init method
        kwargs['model_name'] = self.basename
        return super().get_serializer(*args, **kwargs)
    
    

    # Custom method for success response
    def success_response(self, data, message, status_code=status.HTTP_200_OK):
        return Response({
            'success': True,
            'result': data,
            'message': message
        }, status=status_code)

    # Custom method for failure response
    def failure_response(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            'success': False,
            'message': message
        }, status=status_code)

    # Override create method for POST
    # Override create method for POST
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  # Save the object
            return self.success_response(serializer.data, 'Record created successfully.', status_code=status.HTTP_201_CREATED)
        else:
            return self.failure_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


    # Override retrieve method for GET (single object)
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Get the model name for the serializer
            model_name = self.basename.lower()  # Assuming the basename corresponds to the model name
            serializer_class = get_serializer_class(model_name)
            
            # Use DynamicFieldSerializer for serialization
            serializer = serializer_class(instance, model_name=model_name)
            data = serializer.data  # Get serialized data
            
            return self.success_response(data, 'Record retrieved successfully.')
        
        except Exception as e:
            return self.failure_response(f'Failed to retrieve record: {str(e)}')


    # Override update method for PUT/PATCH
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return self.success_response(serializer.data, 'Record updated successfully.')
        return self.failure_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # Override destroy method for DELETE
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return self.success_response({}, 'Record deleted successfully.')
        except Exception as e:
            return self.failure_response(f'Failed to delete record: {str(e)}')

    # Override list method for GET (list of objects)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())[:10]  # Fetch only the first 10 records
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.success_response(self.get_paginated_response(serializer.data).data, 'Records retrieved successfully.')

        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(serializer.data, 'Records retrieved successfully.')
         
            
import os
from django.conf import settings
from django.http import FileResponse, Http404

def download_file(request, file_name):
  
    file_path = os.path.join(settings.MEDIA_ROOT, 'listingimage', file_name) 
    print("!!!! File path",file_path) ;
    if not os.path.exists(file_path):
        raise Http404("File does not exist.")
    
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response            


from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.conf import settings

class UploadReceiptView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        receipt_image = request.FILES.get('receiptImage')
        if receipt_image:
            # Define the folder where you want to save the image
            service_fee_folder = os.path.join(settings.MEDIA_ROOT, "Servicefee_images")

            # Create the directory if it doesn't exist
            os.makedirs(service_fee_folder, exist_ok=True)

            # Save the file using Django's FileSystemStorage
            fs = FileSystemStorage(location=service_fee_folder)
            filename = fs.save(receipt_image.name, receipt_image)  # Save the file

            # Get the file URL
            file_url = fs.url("Servicefee_images/"+filename)  # This will be relative to the MEDIA_URL setting

            # Return a response with the file URL
            return JsonResponse({'message': 'Upload successful!', 'file_url': file_url})

        else:
            return JsonResponse({'message': 'No image uploaded!'}, status=400)


