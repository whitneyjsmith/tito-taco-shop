from django.shortcuts import render
from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class MEView(APIView):
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer

    def get(self, request):
        """
        Return user details
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
