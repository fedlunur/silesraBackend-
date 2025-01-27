from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import *
from collections import defaultdict
from django.db.models import Q

from rest_framework import generics

class UserRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = [role.name for role in request.user.groups.all()]
        return Response({'roles': roles})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response(status=400, data={'error': str(e)})

class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        clean_data = self.custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def custom_validation(self, data):
        # Implement your custom validation logic here
        return data  # Returning the cleaned data

class UserLogin(APIView):
    permission_classes = [AllowAny]

class UserLogin(APIView):
    permission_classes = [AllowAny]
    
   
    
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
      
            try:
                user = User.objects.get(phone=data['phone'])
            except User.DoesNotExist:
                return Response(
                    {'success': False, 'message': 'No account with this phone has been registered.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

          
            user = authenticate(request, phone=data['phone'], password=data['password'])
            if user is None:
                return Response(
                    {'success': False, 'message': 'Invalid credentials.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

           
            if not user.enabled:
                return Response(
                    {'success': False, 'message': 'Your account has been deactivated.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            
            refresh = RefreshToken.for_user(user)
            login(request, user)
            
            
           
            user.isLoggedIn = 1
            user.save()
            permissions = user.user_permissions.all()
            grouped_permissions = defaultdict(list)

            ignored_models = [
                'permission', 'group', 'contenttype', 'logentry', 'filesattached', 
                'session', 'result', 'outstandingtoken', 'role', 'userlog'
            ]  # Add models you want to ignore here

            for perm in permissions:
                content_type = perm.content_type
                app_label = content_type.app_label
                model = content_type.model

                if model in ignored_models:
                    continue  # Skip the ignored models
                
                perm_codename = perm.codename.split('_', 1)[0] if '_' in perm.codename else perm.codename
                grouped_permissions[model].append(perm_codename)

            user_roles = UserRole.objects.filter(user=user)
            role_data = [{'id': user_role.role.id, 'name': user_role.role.name} for user_role in user_roles]
           
            
           
            
            def find_entity(model, field, user):
    
                filter_kwargs = {field: user}
                entity = model.objects.filter(**filter_kwargs).first()  
                if entity:
                    return {"name": entity.name, "id": entity.id}
                return None   
     
            
            
            return Response({
               # 'refresh': str(refresh),
               # 'access': str(refresh.access_token),     
                'success': True,
                'result': { 
                    'id': user.id,
                   
                     'token':str(refresh.access_token),
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                  
                  
                    'status': user.status,
                 
                    'phone': user.phone,
                    'permissions': grouped_permissions,
                    'role': role_data,
                    'token': str(refresh.access_token),
                    'phone': user.phone,
               
                    'isLoggedIn': user.isLoggedIn , 
                                    
                },
               'message': 'User successfully logged in.',

            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLogout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

