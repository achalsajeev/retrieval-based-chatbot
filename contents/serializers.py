from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

class DomainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domains
        fields = '__all__'
    
    def create(self, data):
        return Domains.objects.create(**data)

    def put(self, instance, data):
        return instance.update(**data)

class IntentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intents
        fields = '__all__'
    
    def create(self, data):
        return Intents.objects.create(**data)

    def put(self, instance, data):
        return instance.update(**data)

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'
    
    def create(self, data):
        return Entity.objects.create(**data)

    def put(self, instance, data):
        return instance.update(**data)

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversations
        fields = '__all__'

    def create(self, data):
        return Conversations.objects.create(**data)

    def put(self, instance, data):
        return instance.update(**data)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
    def create(self, data):
        return Message.objects.create(**data)

class TrainFilesSerializer(ModelSerializer):
    class Meta:
        model = TrainFiles
        fields = '__all__'
    
    def create(self, data):
        return TrainFiles.objects.create(**data)

# class UserSerializer(ModelSerializer):
#     class Meta:
#         fields = ('id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email')
#         model = User
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#         user.set_password(validated_data['password'])
#         user.is_staff = True
#         user.save()

#         return user