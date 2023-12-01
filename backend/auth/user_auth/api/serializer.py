from rest_framework_simplejwt.tokens import Token
from user_auth.models import UserAccount
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class Userserializers(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','first_name','last_name','email','password','is_active','user_image']
        extra_kwargs = {
            'password': {'write_only': True},
        }
            
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance
    

class Loginserializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserImageserializers(serializers.Serializer):
    user_image = serializers.ImageField(
        allow_empty_file=False,
        allow_null=False,
        error_messages={
            'invalid_extension': 'File extension not allowed. Allowed extensions are: bmp, gif, jpeg, jpg, png, tif, tiff, webp, etc.',
        }
    )
    