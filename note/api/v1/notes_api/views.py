from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q
from django.urls import reverse
from api.v1.auth.pagination import StandardResultSetPagination
# local
from notes.models import Note
from api.v1.notes_api.serializers import NoteSerializer



@api_view(['POST'])
def create_note(request):    
    serializer = NoteSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        title = serializer.validated_data['title']
        body = serializer.validated_data['body']
        
        if not Note.objects.filter(title=title, body=body).exists():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_201_CREATED,
                "title": "Create Note",
                "data": serializer.data,
                "list_url": reverse('notes_api:notes'),
                "message": "Note created successfully",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:        
            response_data = {
                "status_code": status.HTTP_406_NOT_ACCEPTABLE,
                "message": "Data already exists.",
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(serializer.errors, status=400) 
    

@api_view(["GET"])
def notes(request):        
    instances = Note.objects.filter(is_deleted=False)
    
    q = request.GET.get("q")
    if q:
        instances = instances.filter(Q(title__icontains=q) | Q(body__icontains=q),is_deleted=False)

    paginator = StandardResultSetPagination()
    paginated_result = paginator.paginate_queryset(instances,request)

    context = {
    "request":request
    }
    serializer = NoteSerializer(paginated_result,many=True,context=context)
    response_data = {
        "status_code" :6000,
        "title" : "Notes List",
        "count" : paginator.page.paginator.count,
        "links" : {
            "next" : paginator.get_next_link(),
            "previous" : paginator.get_previous_link()
        },
        "list_data" : serializer.data
    }

    return Response(response_data)


@api_view(["GET"])
def note(request,pk):
        
    if Note.objects.filter(pk=pk,is_deleted=False).exists():
        instance = Note.objects.get(pk=pk,is_deleted=False)

        context = {
            "request":request
        }
        serializer = NoteSerializer(instance,context=context)
        response_data = {
            "status_code" :200,
            "title" : "Note Details",
            "data" : serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code" :201,
            "title" : "Note Details",
            "message" : "Note not exist"
        }
        return Response(response_data)


@api_view(["PUT"])
def edit_note(request, pk):    
    if Note.objects.filter(pk=pk, is_deleted=False).exists():
        instance = Note.objects.get(pk=pk, is_deleted=False)
        query = request.GET.get("q")
        if query:
            instances = instances.filter(Q(title__icontains=query,body__icontains=query),is_deleted=False)

        serializer = NoteSerializer(instance=instance,data=request.data,partial=True)

        if serializer.is_valid():            
            serializer.save()
            
            response_data = {
                "status_code" : 201,
                "title" : "Edit Note",
                "updated_data" : serializer.data, 
                "list_data" : reverse('notes_api:notes'), 
                "message": "Note Updated successfully",
            }
            return Response(response_data)
        else :
            print("serializer is not valid")
            response_data = {
                "status_code" :status.HTTP_400_BAD_REQUEST, 
                "title" : "Edit Note", 
                "given_data" : serializer.data,
                "Error": serializer.errors,              
                "message": "Serializer not valid",
            }            
            return Response(response_data)           
    else:        
        response_data = {
            "status_code" :6001,   
            "title" : "Edit Note",         
            "message": "Note Not Exists",
        }
        return Response(response_data)


@api_view(["PUT"])
def delete_note(request,pk):    
    if Note.objects.filter(pk=pk, is_deleted=False).exists():
        instance = Note.objects.get(pk=pk,is_deleted=False)        
        Note.objects.filter(pk=pk,is_deleted=False).update(is_deleted=True)        
        response_data = {
            "status_code" :201,
            "title" : "Delete Note",    
            "data" :instance.title,
            "message": "Data Successfully Deleted", 
            "list_data" : reverse('notes_api:notes'),                       
        }        
        return Response(response_data)        
    else:        
        response_data = {
            "status_code" :6001,   
            "title" : "Delete Note",             
            "message": "Note Not Exists",
        }
        return Response(response_data)
    