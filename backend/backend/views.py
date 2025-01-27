from django.http import Http404
from django.db.models import Q
from rest_framework import generics, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
# from .utils import import_all_models
from .utils import genericlist_filds_nested_model
from user_managment.models import *

from products.models import *
from .utils import *
from products.views import *
from datetime import datetime


# Fetch all models from utils.py
# models = import_all_models()

from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound


class GenericPagination(PageNumberPagination):
    page_size_query_param = 'items'

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'result': data,
            'pagination': {
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'count': self.page.paginator.count,
            },
            'message': 'Successfully found all records' if data else 'Record is Empty',
        })

class GenericListAPIView(generics.ListAPIView):
    pagination_class = GenericPagination

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        model = self.get_model(model_name)

        # Check if the request is for the search endpoint
        if 'search' in self.request.path:  # If it's a search request
            query_params = self.request.query_params
            search_query = query_params.get('q', '').strip()  # Get the search query
            fields = query_params.get('fields', '').strip()  # Get the fields

            # Initialize an empty queryset
            queryset = model.objects.none()  # Start with an empty queryset

            # Ensure fields are specified and are not empty
            if search_query and fields:
                fields = fields.split(',')
                # Validate fields against the model's fields
                valid_fields = [f.name for f in model._meta.get_fields() if f.name in fields]

                if valid_fields:  # Only proceed if there are valid fields
                    queries = Q()
                    for field in valid_fields:
                        queries |= Q(**{f"{field}__icontains": search_query})

                    # Apply the filtering based on valid fields and search query
                    queryset = model.objects.filter(queries)
                    queryset = queryset[:10]

            # Return the filtered queryset
            return queryset

        # For the list endpoint, return all records with pagination
        return model.objects.all().order_by('id')
    
    def get_serializer_class(self):
        model_name = self.kwargs['model_name']
        fetched_model = self.get_model(model_name)
        return self.get_serializer_for_model(fetched_model)

    def get_model(self, model_name):
        model_name = model_name.lower()  # Convert model_name to lowercase
        try:
            model_class = model_mapping.get(model_name)  # Get the model class from the mapping
            return model_class
        except KeyError:
            raise Http404("Model not found")

    def get_serializer_for_model(self, fetched_model):
        model_name = fetched_model.__name__.lower()  # Get the model name in lowercase
        allowed_fields ='__all__'  # Get allowed fields or all fields as default

        class NestedSerializer(serializers.ModelSerializer):
            class Meta:
                model = fetched_model
                fields = allowed_fields  # Set fields based on the model name

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in fetched_model._meta.get_fields():
                    # Check if the field is a ForeignKey
                    if field.is_relation and field.many_to_one:
                        related_model = field.related_model
                        # Create a nested serializer for ForeignKey fields
                        self.fields[field.name] = self.create_nested_serializer(related_model)

            def create_nested_serializer(self, related_model):
                related_model_name = related_model.__name__.lower()  # Get related model name in lowercase
                related_fields = genericlist_filds_nested_model.get(related_model_name, ['id'])  # Get allowed fields for related model

                class RelatedSerializer(serializers.ModelSerializer):
                    class Meta:
                        model = related_model
                        fields = related_fields  # Set fields based on the related model name

                return RelatedSerializer()

        return NestedSerializer

    def list(self, request, *args, **kwargs):
        
        page = int(request.query_params.get('page', 1))
        items = int(request.query_params.get('items', 10))
        
        # Update pagination class settings
        self.pagination_class.page_size = items  # Set page size to items
        self.pagination_class.page = page  # Set the page number

        queryset = self.filter_queryset(self.get_queryset())

        if queryset.exists():
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({
                    "success": True,
                    "result": serializer.data,
                    "message": "Successfully found all documents."
                })

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "success": True,
                "result": serializer.data,
                "message": "Successfully found all documents."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "result": [],
                "message": "No documents matched the search criteria."
            }, status=status.HTTP_204_NO_CONTENT)
            
             
def get_counts(request):
 
    result = {
        "enabledUserCount": User.objects.filter(is_active=True).count(),
        "disabledUserCount": User.objects.filter(is_active=False).count(),
        "rolesCount": Role.objects.count(),
        
    
     
    }
    
    return JsonResponse(result)

  
    

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from django.http import Http404
import json
import traceback
from rest_framework import serializers
from backend.utils import donot_include_fields

class AdvancedPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 100
    
class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        model_name = kwargs.pop('model_name', None)  # Get the model name
        super().__init__(*args, **kwargs)
        if model_name in donot_include_fields:
            for field in donot_include_fields[model_name]:
                self.fields.pop(field, None)  # Remove the specified fields

    class Meta:
        model = None  # This will be set dynamically
        fields = '__all__'  # Include all fields by default

    @classmethod
    def get_serializer(cls, model):
        cls.Meta.model = model
        return cls

# Function to get the model class from a mapping
def get_model_class(model_name):
    model_class = model_mapping.get(model_name)
    if model_class is None:
        raise Http404("Model not found")
    return model_class


# Function to get the dynamic serializer class


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
        model_name = kwargs.pop('model_name', None)  # Get the model name
        super().__init__(*args, **kwargs)

        if model_name:
            self.Meta.model = model_mapping.get(model_name)  # Assuming you have model mapping
            
        # Exclude specified fields based on model name
        if model_name in donot_include_fields:
            for field in donot_include_fields[model_name]:
                self.fields.pop(field, None)

        # Automatically add nested serializers for ForeignKey fields
        for field in self.Meta.model._meta.get_fields():
            if field.is_relation and field.many_to_one:  # ForeignKey field
                related_model = field.related_model
                related_model_name = related_model.__name__.lower()

                # Define a nested serializer for the related model
                class RelatedModelSerializer(serializers.ModelSerializer):
                    class Meta:
                        model = related_model
                        fields = genericlist_filds_nested_model.get(related_model_name, ['id'])  # Adjust fields as needed

                # Add the nested serializer to the field
                self.fields[field.name] = RelatedModelSerializer()

def get_serializer_class(model_name):
    return DynamicFieldSerializer

def format_date_string(date_string):
   
    date_only = date_string.split("T")[0]
    # Split the date into components
    year, month, day = date_only.split('-')
    # Format the components to ensure leading zeros
    formatted_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return formatted_date

    try:
        model_name = model_name.lower()
      
        model_config = filter_options_for_appointment_grivance_feedback.get(model_name)
        if not model_config:
            return JsonResponse({'error': 'Invalid model name'}, status=400)

        Model = model_mapping.get(model_config['model'])
        if not Model:
            return JsonResponse({'error': f"Model {model_config['model']} not found"}, status=400)

        expected_fields_from_url = model_config['expected_fields_from_url']
        filter_column_fields = model_config['filter_column_fields']

        # Query params
        global_filter = request.query_params.get('globalFilter', '')
        sorting = request.query_params.get('sorting', '[]')
        size = int(request.query_params.get('size', 10))
        page = int(request.query_params.get('page', 0))  
        field = request.query_params.get('field')  
        value = request.query_params.get('value')  
        filters = request.query_params.get('filters', [])
        print("Filed Id filters =====>  ",Model.__name__.lower() )
        # Construct filter conditions
        filter_conditions = Q(removed=False)  # Base filter
      
        if Model.__name__.lower() in advanced_list_not_require_field_and_value:
          # If field and value are provided, apply them as filters
            if field and value is not None:
                filter_conditions &= Q(**{field: value})
            # Apply expected URL filters if they are provided
            for field in expected_fields_from_url:
                field_value = request.query_params.get(field)
                if field_value:
                    filter_conditions &= Q(**{field: field_value})
        else:
            # Enforce field and value requirement for models not in the list
            if field and value is not None:
                filter_conditions &= Q(**{field: value})
                # Apply additional URL filters if available
                for field in expected_fields_from_url:
                    try:
                        field_value = request.query_params.get(field)
                        if field_value:
                            filter_conditions &= Q(**{field: field_value})
                    except Exception as e:
                        print(f"Error processing field '{field}': {e}")
            else:
                # Return an error if field and value are required but not provided
                return Response({"status": False, "data": [], "error": "Field is needed"})

        # Continue with additional filtering, pagination, etc.

        

        # Additional filters
        
        
        try:
            filters = json.loads(filters) if filters else []
        except json.JSONDecodeError:
            filters = []
        print("Filed Id filters =====>!!!  ",filters )
        for filter_item in filters:
            field_id = filter_item.get('id')
            field_value = filter_item.get('value')
            print("Filed Id =====>  ",field_id)
            if field_id and field_value is not None:
            # Check if the field is a date range filter
                if field_id == "dateHappened" and isinstance(field_value, list) and len(field_value) == 2:
                    print("Filed Id =====>  ",field_id)
                    try:
                        # Parse the start and end dates
                        
                        start_date_str = format_date_string(field_value[0])
                        end_date_str = format_date_string(field_value[1])
                        
                        # Parse the dates
                        start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
                        end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                        # Apply date range filtering
                        filter_conditions &= Q(**{f"{field_id}__gte": start_date, f"{field_id}__lte": end_date})
                    except ValueError as e:
                        print(f"Error parsing dates for field '{field_id}': {e}")
                else:
                    # Default to text-based filtering for other fields
                    filter_conditions &= Q(**{f"{field_id}__icontains": field_value})
        # Apply text-based filtering (e.g., globalFilter)
        if global_filter:
            global_filter_conditions = Q()
            for column in model_config['filter_column_fields']:
                global_filter_conditions |= Q(**{f"{column}__icontains": global_filter})
            filter_conditions &= global_filter_conditions

        # Sorting logic
        ordering = ['created']
        if sorting:
            try:
                sorting = json.loads(sorting)
            except json.JSONDecodeError:
                sorting = []

            order_list = []
            for sort in sorting:
                sort_field = sort.get('id')
                sort_direction = '-' if sort.get('desc') else ''
                order_list.append(f"{sort_direction}{sort_field}")
            ordering = order_list

        queryset = Model.objects.filter(filter_conditions).order_by(*ordering)
        total_count = queryset.count()
        total_pages = (total_count // size) + (1 if total_count % size else 0)
        start = page * size
        end = start + size
        paginated_queryset = queryset[start:end]

        serializer = get_serializer_class(model_name)(paginated_queryset, many=True, model_name=model_name)

        pagination = {
            "page": page,
            "pages": total_pages,
            "count": total_count,
        }

        return Response({
            "success": True,
            "data": serializer.data,
            "meta": pagination,
        }, status=200)

    except Http404:
        return Response({"data": [], "error": "Not found"}, status=404)
    except Exception as err:
        print(traceback.format_exc())
        return Response({"data": [], "error": str(err)}, status=500)

    """
    Primary model search based on Foeign key value 
    """
from django.core.exceptions import ObjectDoesNotExist   
from django.views.decorators.csrf import csrf_exempt



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user    
   
 
class PasswordChangeView(generics.UpdateAPIView):

    serializer_class = PasswordChangeSerializer
    model = User
    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Change the password
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({'Success': True,'data':serializer.data,'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

from django.core.paginator import Paginator, EmptyPage
 


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        model_name = kwargs.pop('model_name', None)
        super().__init__(*args, **kwargs)
        if model_name:
            self.Meta.model = model_mapping.get(model_name)  # Use model_mapping to get the model class
        print("Hey there How are you !!!!1" )
        # Exclude specified fields based on model name
        if model_name in donot_include_fields:
            for field in donot_include_fields[model_name]:
                self.fields.pop(field, None)

        # Automatically add nested serializers for ForeignKey fields
        if self.Meta.model:
            for field in self.Meta.model._meta.get_fields():
                if field.is_relation and field.many_to_one:  # ForeignKey field
                    related_model = field.related_model
                    related_model_name = related_model.__name__.lower()

                    # Define a nested serializer for the related model
                    class RelatedModelSerializer(serializers.ModelSerializer):
                        class Meta:
                            model = related_model
                            fields = genericlist_filds_nested_model.get(related_model_name, ['id'])

                    # Add the nested serializer to the field
                    self.fields[field.name] = RelatedModelSerializer()




    def get_serializer_class(self):
        return DynamicFieldSerializer

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('items', 10))
        skip = (page - 1) * limit

        filter_key = request.query_params.get('filter')
        equal = request.query_params.get('equal')
        user_type = request.query_params.get('userType')
        current_user_id = request.query_params.get('currentUserId')
        query = {'removed': False}
        
        if filter_key and equal:
            query[filter_key] = equal
    
      
        paginator = Paginator(unique_users, limit)
        
        try:
            paginated_results = paginator.page(page)
        except EmptyPage:
            paginated_results = []

        # Serialize the paginated data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(paginated_results, model_name='user', many=True)
        
            
            # Use DynamicFieldSerializer for serialization
      
        pagination = {
            "page": page,
            "pages": paginator.num_pages,
            "count": paginator.count,
        }
        
        return Response({
            "success": True,
            "result": serializer.data,  # Serialized paginated data
            "pagination": pagination,
            "message": "Users have been successfully loaded."
        })

    def fetch_users_for_organization_admin(self, current_user_id, query):
        organization = Organization.objects.filter(admin=current_user_id).first()
        if not organization:
            return []
        org_users = User.objects.filter(subTypeId=organization.id, superType=SUPER_TYPE_ENUM['CITY'], **query)
        unit_users = User.objects.filter(subTypeId__in=Unit.objects.filter(organization=organization.id).values_list('id', flat=True), superType=SUPER_TYPE_ENUM['CITY'], **query)
        dept_users = User.objects.filter(subTypeId__in=Department.objects.filter(unit__in=unit_users.values_list('subTypeId', flat=True)).values_list('id', flat=True), superType=SUPER_TYPE_ENUM['CITY'], **query)
        return org_users | unit_users | dept_users

    def fetch_users_for_subcity_admin(self, current_user_id, query):
        subcity = Subcity.objects.filter(admin=current_user_id).first()
        if not subcity:
            return []
        subcity_users = User.objects.filter(subTypeId=subcity.id, superType=SUPER_TYPE_ENUM['SUB_CITY'], **query)
        pool_users = User.objects.filter(subTypeId__in=Pool.objects.filter(subcity=subcity.id).values_list('id', flat=True), superType=SUPER_TYPE_ENUM['SUB_CITY'], **query)
        office_users = User.objects.filter(subTypeId__in=Office.objects.filter(pool__in=pool_users.values_list('subTypeId', flat=True)).values_list('id', flat=True), superType=SUPER_TYPE_ENUM['SUB_CITY'], **query)
        return subcity_users | pool_users | office_users

    def fetch_users_for_wereda_admin(self, current_user_id, query):
        wereda = Wereda.objects.filter(admin=current_user_id).first()
        if not wereda:
            return []
        wereda_users = User.objects.filter(subTypeId=wereda.id, superType=SUPER_TYPE_ENUM['WEREDA'], **query)
        wereda_office_users = User.objects.filter(subTypeId__in=Weredaoffice.objects.filter(wereda=wereda.id).values_list('id', flat=True), superType=SUPER_TYPE_ENUM['WEREDA'], **query)
        return wereda_users | wereda_office_users  
