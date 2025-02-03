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
import os
from django.core.files import File
from django.conf import settings
from rest_framework import serializers
class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # This will be set dynamically
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Get the model name passed in kwargs
        model_name = kwargs.pop('model_name', None)
        super().__init__(*args, **kwargs)

        # Dynamically set the model if model_name is provided
        if model_name:
            self.Meta.model = model_mapping.get(model_name)

        # Handle exclusion of specific fields
        if model_name in donot_include_fields:
            for field in donot_include_fields[model_name]:
                self.fields.pop(field, None)

        # Handle ForeignKey fields dynamically
        if self.Meta.model:
            for field in self.Meta.model._meta.get_fields():
               #  print("=====> Checking the field", field)
                # Ensure we are dealing with a ForeignKey that has a related model
                if field.is_relation and field.many_to_one and hasattr(field, 'related_model') and field.related_model:
                   #  print("=====> Adding RelationField for:", field)
                    self.fields[field.name] = self.RelationField(field.related_model)

    class RelationField(serializers.PrimaryKeyRelatedField):
        def __init__(self, model, **kwargs):
            if not model:
                raise ValueError("Model cannot be None")
          
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
        images_data = request.data.pop('images', [])  # Extract images from request
        recept_images = request.data.pop('reciptimages', [])  # Extract receipt images
        serializer = self.get_serializer(data=request.data)

        print("!!!!!!!! Image data before parsing ", images_data)

        if serializer.is_valid():
            instance = serializer.save()  # Save the main object (e.g., ServiceFee)

            # Handle general images (images_data)
            if images_data:
                content_type = ContentType.objects.get_for_model(instance)
                print("Image data before parsing ", images_data)
                for image_data in images_data:
                    image_path = image_data.get('imagepath')
                    print("££££££ look image_path ", image_path)
                    if image_path:
                        # Sanitize the image path and ensure it doesn't attempt path traversal
                        image_instance = ListingImage.objects.create(
                                content_type=content_type,
                                object_id=instance.id,
                                imagepath=image_path  # Store just the filename
                            )
                        image_instance.save()
                        
 
            # Handle receipt images (recept_images)
            if recept_images:
                for recept_image_data in recept_images:
                    image_path = recept_image_data.get('imagepath')
                    servicefeeBank=recept_image_data.get('servicefeeBank')
                    servicefeeBank_instance = CustomerBank.objects.get(id=servicefeeBank)
                    feeReciptRefnumber=recept_image_data.get('feeReciptRefnumber')
                    
                    if image_path:
                         recipt_instance = ServiceFee.objects.create(
                                contentType=content_type,
                                object_id=instance.id,
                                servicefeeBank=servicefeeBank_instance,
                                feeReciptImagePath=image_path,  # Store just the filename
                                feeReciptRefnumber=feeReciptRefnumber,
                            )
                         recipt_instance.save()
                       

            return self.success_response(serializer.data, 'Record created successfully.', status_code=status.HTTP_201_CREATED)
        else:
            return self.failure_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    
 
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
    from django.contrib.contenttypes.models import ContentType

    def list(self, request, *args, **kwargs):
        print("!!! list is called  =======> ")
        
        # Get the queryset for the current model (Car, House, etc.)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        # Get the content type for the current model (e.g., Car, House)
        content_type = ContentType.objects.get_for_model(queryset.model)
        
        # Serialize the queryset with all fields
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            
            # Add images to each serialized object
            for item in data:
                object_id = item['id']  # Ensure 'id' is the primary key field
                images = ListingImage.objects.filter(content_type=content_type, object_id=object_id)
                
                # Add related images data
                item['images'] = [{'id': image.id, 'imagepath': image.imagepath} for image in images]
            
            return self.success_response(self.get_paginated_response(data).data, 'Records retrieved successfully.')

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Add images to each serialized object
        for item in data:
            object_id = item['id']
            images = ListingImage.objects.filter(content_type=content_type, object_id=object_id)
            
            # Add related images data
            item['images'] = [{'id': image.id, 'imagepath': image.imagepath} for image in images]

        return self.success_response(data, 'Records retrieved successfully.')

    
import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.utils._os import safe_join

def download_file(request, image_type, file_path):
    print("!!!!! Image Type",image_type,"file_path",file_path);
    if image_type not in ['Servicefee_images', 'Listing_images','listingimage']:  # Add more image types as needed
        raise Http404("Invalid ImageType provided.")
    
    try:
        # Safely join the media root with the image folder and file path
        folder_path = os.path.join(settings.MEDIA_ROOT, image_type)  # Folder path (e.g., 'listingimage')
        full_path = safe_join(folder_path, file_path)  # Full path to the file inside the folder

        # Check if the file exists
        if not os.path.exists(full_path):
            raise Http404("File does not exist.")
        
        # Return the file as a downloadable response
        response = FileResponse(open(full_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_path)}"'
        return response
    
    except Exception as e:
        raise Http404(f"Error accessing file: {str(e)}")      


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


from rest_framework import serializers

class ModelContentTypeSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    content_type_id = serializers.IntegerField()



from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound

class ModelContentTypeView(APIView):
    def get(self, request, model_name, *args, **kwargs):
        # Convert model_name to lowercase to match the model_mapping keys
        model_name = model_name.lower()

        # Attempt to get the model class from model_mapping
        model_class = model_mapping.get(model_name)
        print("The model mapping found is !!!!! ", model_class)

        if not model_class:
            raise NotFound(detail="Model not found")

        # Get the content type for the model
        content_type = ContentType.objects.get_for_model(model_class)

        # Return model name and content type ID
        return Response({
            "model_name": model_class.__name__,
            "content_type_id": content_type.id
        }, status=status.HTTP_200_OK)