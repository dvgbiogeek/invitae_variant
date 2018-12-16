from django.db import models


class Gene(models.Model):
    """
    Initial model for a gene/transcript (Genetic information where there is no variant).
    """
    gene_id = models.AutoField(primary_key=True)
    gene_name = models.CharField(max_length=24, blank=True)


class Transcript(models.Model):
    """
    Initial model for transcripts
    """
    transcript_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True)


class Allele(models.Model):
    allele_id = models.AutoField(primary_key=True)
    allele = models.CharField(max_length=16, blank=True)


class Mapping(models.Model):
    """
    Model for other mappings.
    """
    mapping_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True)


class Variant(models.Model):
    """
    Initial model for variants.
    """
    variant_id = models.AutoField(primary_key=True)
    mappings = models.ManyToManyField(
        Mapping,
        through="MappingJoinTable",
        through_fields=('variant', 'mapping'),
    )
    ref_allele = models.ForeignKey(Allele, on_delete=models.PROTECT, related_name="ref_allele")
    alt_allele = models.ForeignKey(Allele, on_delete=models.PROTECT, related_name="alt_allele")
    reported_ref = models.ForeignKey(Allele, on_delete=models.PROTECT, related_name="reported_ref")
    reported_alt = models.ForeignKey(Allele, on_delete=models.PROTECT, related_name="reported_alt")
    protein_change = models.CharField(max_length=32, blank=True)


class MappingJoinTable(models.Model):
    mapping = models.ForeignKey(Mapping, on_delete=models.PROTECT)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    nucleotide_change = models.BooleanField()


class GenomicLocation(models.Model):
    """
    Initial model for the location of a variant mapped to the genome.
    """
    genomic_location_id = models.AutoField(primary_key=True)
    assembly = models.CharField(max_length=8, blank=True)
    chromosome = models.CharField(max_length=8, blank=True)
    start = models.CharField(max_length=32, blank=True)
    stop = models.CharField(max_length=32, blank=True)
    transcripts = models.ManyToManyField(
        Transcript,
        through="TranscriptJoinTable",
        through_fields=('genomic_location', 'transcript'),
    )
    region = models.CharField(max_length=64, blank=True)


class TranscriptJoinTable(models.Model):
    transcript = models.ForeignKey(Transcript, on_delete=models.PROTECT)
    genomic_location = models.ForeignKey(GenomicLocation, on_delete=models.PROTECT)
    accession = models.BooleanField()


class Source(models.Model):
    """
    Model for Variant Source information.
    """
    source_id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=16, blank=True)  # Note: Have not noticed any empty fields here, but not unique
    last_eval = models.CharField(max_length=16, blank=True)
    last_updated = models.CharField(max_length=16, blank=True)
    source_url = models.URLField(blank=True)


class Classification(models.Model):
    """
    Model for Variant Classification
    """
    classification_id = models.AutoField(primary_key=True)
    # Max currently length 58.
    name = models.CharField(max_length=128, blank=True)


class ExtraProperties(models.Model):
    """
    Model to add extra properties.

    These seem to be uncommon, but have significant text when present. Breaking out into
    seperate table for size.
    """
    extra_props_id = models.AutoField(primary_key=True)
    submitter_comments = models.TextField(blank=True)
    alias = models.CharField(max_length=256, blank=True)


class GeneVariantInfo(models.Model):
    """
    Join table to link all the tables together.
    """
    gene_variant_info_id = models.AutoField(primary_key=True)
    # To serve as an identifier for each entry since none of the fields are true identifier fields
    uuid_for_variant = models.CharField(max_length=48)
    gene = models.ForeignKey(Gene, on_delete=models.PROTECT)
    # many to many
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    genomic_location = models.ForeignKey(GenomicLocation, on_delete=models.PROTECT)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    reported_classification = models.ForeignKey(Classification, on_delete=models.PROTECT, related_name="reported")
    inferred_classification = models.ForeignKey(Classification, on_delete=models.PROTECT, related_name="inferred")
    extra_properties = models.ForeignKey(ExtraProperties, on_delete=models.PROTECT)
