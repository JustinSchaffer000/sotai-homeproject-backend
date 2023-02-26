from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        label="Name",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
            
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
    
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        
        return user
    