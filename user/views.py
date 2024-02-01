from django.shortcuts import render
from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer

class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    
    def get_queryset(self):
        print("USER GET QUERYSET")
        return super().get_queryset().filter(id=self.request.user.id)

