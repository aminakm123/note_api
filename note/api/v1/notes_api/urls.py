from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.v1.notes_api import views


app_name = 'notes_api'
urlpatterns = [  
    path('note/create/', views.create_note, name='create_note'),      
    path('notes/', views.notes, name='notes'),
    path('note/<int:pk>/', views.note, name='note'),
    path('note/edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('note/delete/<int:pk>/', views.delete_note, name='delete_note'),    
]
urlpatterns = format_suffix_patterns(urlpatterns)