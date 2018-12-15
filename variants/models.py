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
    transcript = models.CharField(max_length=256, blank=True)


class OtherMappings(models.Model):
    """
    Model for other mappings.
    """
    other_mappings_id = models.AutoField(primary_key=True)
    other_mapping = models.TextField(blank=True)


class GenomicLocation(models.Model):
    """
    Initial model for the location of a variant mapped to the genome.
    """
    genomic_location_id = models.AutoField(primary_key=True)
    assembly = models.CharField(max_length=8, blank=True)
    chromosome = models.CharField(max_length=8, blank=True)
    start = models.CharField(max_length=24, blank=True)
    stop = models.CharField(max_length=24, blank=True)
    accession = models.CharField(max_length=24, blank=True)


class Variant(models.Model):
    """
    Initial model for variants.
    """
    variant_id = models.AutoField(primary_key=True)
    nucleotide_change = models.CharField(max_length=24, blank=True)
    protein_change = models.CharField(max_length=24, blank=True)
    ref_allele = models.CharField(max_length=24, blank=True)
    alt_allele = models.CharField(max_length=24, blank=True)
    reported_ref = models.CharField(max_length=24, blank=True)
    reported_alt = models.CharField(max_length=24, blank=True)


class Source(models.Model):
    """
    Model for Variant Source information.
    """
    source_id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=24, blank=True)  # Note: Have not noticed any empty fields here, but not unique
    last_eval = models.CharField(max_length=24, blank=True)
    last_updated = models.CharField(max_length=24, blank=True)
    source_url = models.URLField(blank=True)


class Classification(models.Model):
    """
    Model for Variant Classification
    """
    classification_id = models.AutoField(primary_key=True)
    reported = models.CharField(max_length=256, blank=True)
    inferred = models.CharField(max_length=256, blank=True)


class ExtraProperties(models.Model):
    """
    Model to add extra properties
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
    transcript = models.ForeignKey(Transcript, on_delete=models.PROTECT)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    genomic_location = models.ForeignKey(GenomicLocation, on_delete=models.PROTECT)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    other_mappings = models.ForeignKey(OtherMappings, on_delete=models.PROTECT)
    extra_properties = models.ForeignKey(ExtraProperties, on_delete=models.PROTECT)
