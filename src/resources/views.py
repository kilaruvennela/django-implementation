from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.

from .models import Resource 
from .serializers import ResourceSerializer

class UnicornViewSet(viewsets.ModelViewSet):

    # queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        user = self.request.user
        return Resource.objects.filter(user=user)

