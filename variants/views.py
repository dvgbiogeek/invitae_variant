from django.shortcuts import render

from rest_framework import viewsets

from variants.models import GeneVariantInfo, Gene
from variants.serializers import GeneSerializer, GeneVariantInfoSerializer


class GeneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for genes to be viewed.
    """
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    http_method_names = ['get']


class GeneVariantInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for gene variant info to be viewed.
    """
    queryset = GeneVariantInfo.objects.all()
    serializer_class = GeneVariantInfoSerializer
    http_method_names = ['get']