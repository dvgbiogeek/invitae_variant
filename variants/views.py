from django.shortcuts import render

from variants.models import GeneVariantInfo

def index(request):
    """
    View for the Recipe index page.
    TODO: Should limit the number of recipes.
    :param request:
    :return:
    """
    gene_variants = GeneVariantInfo.objects.all()
    context = {'gene_variants': gene_variants}
    return render(request, 'index.html', context)
