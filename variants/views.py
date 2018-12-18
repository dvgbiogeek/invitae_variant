from django.shortcuts import render

from rest_framework import viewsets

from variants.models import GeneVariantInfo, Gene
from variants.serializers import GeneSerializer, GeneVariantInfoSerializer


# def index(request):
#     """
#     View for the Recipe index page.
#     TODO: Should limit the number of recipes.
#     :param request:
#     :return:
#     """
#     gene_variants = GeneVariantInfo.objects.all()
#     context = {'gene_variants': gene_variants}
#     return render(request, 'index.html', context)


class GeneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for genes to be viewed.
    """
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer


class GeneVariantInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for gene variant info to be viewed.
    """
    queryset = GeneVariantInfo.objects.all()
    serializer_class = GeneVariantInfoSerializer
