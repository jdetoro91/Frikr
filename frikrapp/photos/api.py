# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer, PhotoListSerializer, FileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from models import Photo, VISIBILITY_PUBLIC, File
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from permissions import UserPermission
from django.db.models import Q
from django.core.mail import send_mail


class UserListAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.DATA) # en lugar request.POST
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDetailAPI(APIView):

    permission_classes = (UserPermission,)


    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class PhotoAPIQueryset:


    def get_queryset(self):
        """
        Devuelve un queryset en función de varios criterios
        """
        if self.request.user.is_superuser:
            return Photo.objects.all()
        elif self.request.user.is_authenticated():
            return Photo.objects.filter(Q(visibility=VISIBILITY_PUBLIC) | Q(owner=self.request.user))
        else:
            return Photo.objects.filter(visibility=VISIBILITY_PUBLIC)




class PhotoListAPI(PhotoAPIQueryset, ListCreateAPIView):
    """
    Implementa el API de listado (GET) y creación (POST) de fotos
    (Sí, en serio)
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)



    def get_serializer_class(self):
        if self.request.method == "POST":
            return PhotoSerializer
        else:
            return self.serializer_class
        #return PhotoSerializer if self.request.method == "POST" else self.serializer_class



    def pre_save(self, obj):
        """
        Asigna la autoría de la foto al usuario autenticado al crearla
        """
        obj.owner = self.request.user


class PhotoDetailAPI(PhotoAPIQueryset, RetrieveUpdateDestroyAPIView):
    """
    Implementa el API de detalle (GET), actualización (PUT), y borrado (DELETE)
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)




class PhotoUploadAPI(CreateAPIView):

    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated,)





















