from rest_framework import serializers
from contacts import models as contacts_models

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