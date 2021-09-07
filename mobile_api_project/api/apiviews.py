from django.contrib.auth import get_user_model
from django.core.validators import validate_email

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from . import serializers
from django.contrib.auth import authenticate, login, logout

import json


from api import serializers
from contacts import models as contacts_models

import re

def is_email(email):
    """Checks if email is valid"""
    try:
        validate_email(email)
        return True
    except Exception:
        return False


class ContactsView(APIView):
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



# class NotesView(ListCreateAPIView):
#     queryset = contacts_models.Note.objects.all()
#     serializer_class = serializers.NoteSerializer



# class NoteView(RetrieveDestroyAPIView):
#     queryset = contacts_models.Note.objects.all()
#     serializer_class = serializers.NoteSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_with_token(request):
    res = {} # response data returned by the view
    message = ''
    success = False
    token = None

    data = json.loads(request.body)
    last_name = data['last_name']
    first_name = data['first_name']
    email = data['email']
    pwd1 = data['pwd1']
    pwd2 = data['pwd2']

    if not last_name or last_name.isspace() or not first_name or first_name.isspace() or not email or email.isspace() or not pwd1 or pwd1.isspace() or not pwd2 or pwd2.isspace():
        res['message'] = 'Erreur!: Veuillez remplir les champs vides'
        res['success'] = success
        return Response(res)
    elif not re.fullmatch('[A-Za-z ]+', last_name):
        res['message'] = 'Erreur!: Veuillez saisir un nom valide'
        res['success'] = success
        return Response(res)
    elif not re.fullmatch('[A-Za-z ]+', first_name):
        res['message'] = 'Erreur!: Veuillez saisir un prénom valide'
        res['success'] = success
        return Response(res)
    elif not is_email(email):
        res['message'] = 'Erreur!: Veuillez saisir un email valide'
        res['success'] = success
        return Response(res)
    elif pwd1 != pwd2:
        res['message'] = 'Erreur!: Les mots de passe ne sont pas identiques'
        res['success'] = success
        return Response(res)
    else:
        user_data = {
            'username':email,
            'last_name':last_name,
            'first_name':first_name,
            'password':pwd1
        }

        serializer = serializers.UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get_or_create(user=user)[0].key
            success = True
            res['message'] = 'Inscription éffectuée avec succès'
            res['success'] = success
            res['token'] = token
            return Response(res)
        else: return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    message = ''
    success = False

    res = {}
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)
    if user:
        try:
            token = Token.objects.get_or_create(user=user)[0].key
            login(request, user)
            message = 'utilisateur connecté'
            success = True
            res['message'] = message
            res['username'] = user.username
            res['last_name'] = user.last_name
            res['first_name'] = user.first_name
            res['success'] = success
            res['token'] = token

            return Response(res, status=status.HTTP_200_OK)
        except Exception:
            message = "Erreur!: Cet utilisateur n'existe pas"
            res['message'] = message
            res['success'] = success
            return Response(res)
    else:
        message = "Erreur!: Email ou mot de passe incorrect"
        res['message'] = message
        res['success'] = success
        return Response(res)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sign_out(request):
    message = ''

    request.user.auth_token.delete()
    logout(request)
    message = 'utilisateur déconnecté'

    return Response({'mesdage':message})