# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer, PhotoListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from models import Photo


class UserListAPI(APIView):

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

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PhotoListAPI(ListCreateAPIView):
    """
    Implementa el API de listado (GET) y creación (POST) de fotos
    (Sí, en serio)
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer


    def get_serializer_class(self):
        if self.request.method == "POST":
            return PhotoSerializer
        else:
            return self.serializer_class
        #return PhotoSerializer if self.request.method == "POST" else self.serializer_class


class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Implementa el API de detalle (GET), actualización (PUT), y borrado (DELETE)
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
























