from rest_framework import serializers
from contacts import models as contacts_models
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contacts_models.Contact
        fields = '__all__'
        depth = 1


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = contacts_models.Note
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username', 'email', 'password')
            extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            # Création de token a la création de l'utilisateur
            Token.objects.create(user=user)
            return user
