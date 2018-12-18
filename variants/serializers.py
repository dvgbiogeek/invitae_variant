from rest_framework import serializers

from variants.models import Gene, GeneVariantInfo, Mapping, Transcript, Variant, Allele


class GeneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gene
        fields = ('gene_name',)


class TranscriptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transcript
        fields = ('transcript_name',)


class MappingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mapping
        fields = ('mapping_name',)


class AlleleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Allele
        fields = ('allele',)


class VariantExtrasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Variant
        fields = ('ref_allele', 'alt_allele', 'reported_ref', 'reported_alt', 'protein_change')


class GeneVariantInfoSerializer(serializers.HyperlinkedModelSerializer):
    transcripts = TranscriptSerializer(read_only=True, many=True)
    mappings = MappingSerializer(read_only=True, many=True)
    # variant_extras = VariantExtrasSerializer(allow_null=True)

    class Meta:
        model = GeneVariantInfo
        fields = ('gene', 'mappings', 'transcripts', )
                  #  'variant_extras', 'genomic_location', 'source',
                  #  'reported_classification', 'inferred_classification', 'extra_properties')






