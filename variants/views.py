from django.shortcuts import render

from rest_framework import generics

from variants.models import GeneVariantInfo, Gene
from variants.serializers import GeneSerializer, GeneVariantInfoSerializer


class GeneList(generics.ListAPIView):
    """
    API endpoint for genes to be viewed.
    """
    serializer_class = GeneSerializer
    lookup_field = 'gene_name'

    def get_queryset(self):
        gene = self.kwargs['gene']
        queryset = Gene.objects.filter(gene_name__startswith=gene)
        return queryset


class GeneVariantInfoList(generics.ListCreateAPIView):
    """
    API endpoint for gene variant info to be viewed.
    """
    serializer_class = GeneVariantInfoSerializer
    lookup_field = 'gene_name'

    def get_queryset(self):
        gene_name = self.kwargs['gene']
        queryset = GeneVariantInfo.objects.filter(gene__gene_name=gene_name)
        return queryset


class GeneVariantInfoAllList(generics.ListCreateAPIView):
    """
    API endpoint for gene variant info to be viewed.
    """
    serializer_class = GeneVariantInfoSerializer
    ordering = ['gene_variant_id']

    def get_queryset(self):
        queryset = GeneVariantInfo.objects.all()
        return queryset
