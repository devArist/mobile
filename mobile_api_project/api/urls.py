from django.urls import path
from . import apiviews
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('contacts', apiviews.ContactsView.as_view(), name='contacts'),
    path('contact/<int:pk>', apiviews.ContactView.as_view(), name='contact'),
    path('signup', apiviews.create_user_with_token, name='signup'),
    path('signin', apiviews.signin, name='signin'),
    path('signout', apiviews.sign_out, name='signout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
