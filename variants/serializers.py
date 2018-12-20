from rest_framework import serializers

from variants.models import Gene, GeneVariantInfo, Mapping, Transcript, Variant, Allele, GenomicLocation, Source, \
    Classification, ExtraProperties


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
    ref_allele = AlleleSerializer()
    alt_allele = AlleleSerializer()
    reported_ref = AlleleSerializer()
    reported_alt = AlleleSerializer()

    class Meta:
        model = Variant
        fields = ('ref_allele', 'alt_allele', 'reported_ref', 'reported_alt', 'protein_change')


class GenomicLocationSerializer(serializers.HyperlinkedModelSerializer):
    assembly = serializers.StringRelatedField()
    chromosome = serializers.StringRelatedField()
    start = serializers.StringRelatedField()
    stop = serializers.StringRelatedField()
    region = serializers.StringRelatedField()

    class Meta:
        model = GenomicLocation
        fields = ('assembly', 'chromosome', 'start', 'stop', 'region')


class SourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Source
        fields = ('source', 'last_eval', 'last_updated', 'source_url')


class ClassificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Classification
        fields = ('name',)


class ExpertPropertiesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExtraProperties
        fields = ('submitter_comments', 'alias')


class GeneVariantInfoSerializer(serializers.ModelSerializer):
    gene = GeneSerializer()
    transcripts = TranscriptSerializer(read_only=True, many=True)
    mappings = MappingSerializer(read_only=True, many=True)
    variant_extras = VariantExtrasSerializer()
    genomic_location = GenomicLocationSerializer()
    source = SourceSerializer()
    reported_classification = ClassificationSerializer()
    inferred_classification = ClassificationSerializer()
    extra_properties = ExpertPropertiesSerializer()

    class Meta:
        model = GeneVariantInfo
        fields = ('gene', 'mappings', 'transcripts', 'variant_extras', 'genomic_location', 'source',
                  'reported_classification', 'inferred_classification', 'extra_properties')
