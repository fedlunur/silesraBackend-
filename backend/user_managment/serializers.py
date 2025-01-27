from django.forms import ValidationError
from rest_framework import serializers

from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .validations import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # or use serializers.PrimaryKeyRelatedField()
    role = serializers.StringRelatedField()  # or use serializers.PrimaryKeyRelatedField()

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']


#used to create access token and refresh once valid user found 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token['first_name'] = user.first_name
     
        token['id'] = str(user.id)
        token['status'] = user.status
   
        token['phone'] = user.phone
   
        #Group permissions by model
        permissions = user.user_permissions.all()
        grouped_permissions = defaultdict(list)
        for perm in permissions:
            model = perm.content_type.model
            grouped_permissions[model].append(perm.codename)

        token['permissions'] = grouped_permissions

        # Add user roles
        token['roles'] = [{'id': role.role.id, 'name': role.role.name} for role in user.userrole_set.all()]

        return token

#Account creation Serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
          
            phone=validated_data['phone']

        )
        
       #beacuse we need to hash so this set password 
       
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        required=True,
    
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
  
    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        if not phone or not password:
            raise serializers.ValidationError("phone and password are required.")
        
        user = authenticate(phone=phone, password=password)
      
        if not user:
            raise serializers.ValidationError("Invalid phone or password.")
        
        return {'user': user}    
    
