from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api import serializers
from contacts import models as contacts_models


class ContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = contacts_models.Contact.objects.filter(
            user=request.user
        )
        serializer = serializers.ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')
        contact = contacts_models.Contact(
            name=name,
            email=email,
            phonenumber=phonenumber,
            user=request.user
        )
        contact.save()
        serializer = serializers.ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            contact = contacts_models.Contact.objects.get(
                pk=pk,
                user=request.user
            )
            serializer = serializers.ContactSerializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except contacts_models.Contact.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        name = request.data.get('name')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')
        contact = contacts_models.Contact.objects.get(
            pk=pk,
            user=request.user
        ).update(
            name=name,
            email=email,
            phonenumber=phonenumber
        )
        serializer = serializers.ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_202_UPDATED)
    
    def delete(self, request, pk):
        contacts_models.Contact.objects.get(
            pk=pk,
            user=request.user
        ).delete()
        return Response(status=status.HTTP_203_DELETED)



class NotesView(ListCreateAPIView):
    queryset = contacts_models.Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated]


class NoteView(RetrieveDestroyAPIView):
    queryset = contacts_models.Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [IsAuthenticated]


class UserView(APIView):
    def post(self, request):
        last_name = request.data.get('last_name')
        first_name = request.data.get('first_name')
        email = request.data.get('email')
        pwd1 = request.data.get('pwd1')
        pwd2 = request.data.get('pwd2')

        get_user_model().create_user(
            last_name=last_name,
            first_name=first_name,
            username=email,
            password=pwd1
        )

        return Response(status=status.HTTP_201_CREATED)