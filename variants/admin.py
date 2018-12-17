from django.contrib import admin

from variants.models import Gene, Transcript, GenomicLocation, TranscriptJoinTable, Allele, Mapping, MappingJoinTable, \
    Source, ExtraProperties, Variant, Classification, GeneVariantInfo

admin.site.register(Gene)
admin.site.register(GeneVariantInfo)
admin.site.register(Transcript)
admin.site.register(GenomicLocation)
