from django.urls import path
from . import apiviews


urlpatterns = [
    path('contacts', apiviews.ContactsView.as_view(), name='contacts'),
    path('contact/<int:pk>', apiviews.ContactView.as_view(), name='contact'),
    # path('notes', apiviews.NotesView.as_view(), name='notes'),
    # path('note/<int:pk>', apiviews.NotesView.as_view(), name='notes'),
]
