import unittest
from django.test import TestCase

from variants.models import Gene, Transcript, Allele, GenomicLocation, Mapping, Variant, Source, Classification, \
    ExtraProperties, GeneVariantInfo, MappingJoinTable, TranscriptJoinTable


class GeneModelCreateTests(TestCase):
    def test_add_gene(self):
        """
        Test adding gene names to the Gene model
        :return:
        """
        Gene.objects.get_or_create(gene_name='CDKL5')
        last_entry = Gene.objects.last()
        self.assertEqual(last_entry.gene_name, 'CDKL5')

    def test_add_gene_blank(self):
        """
        Test adding blank gene names to the Gene model
        :return:
        """
        Gene.objects.get_or_create(gene_name='')
        last_entry = Gene.objects.last()
        self.assertEqual(last_entry.gene_name, '')


class TranscriptModelCreateTests(TestCase):
    def test_add_transcript(self):
        """
        Test adding transcript to the transcript model.
        :return:
        """
        Transcript.objects.get_or_create(transcript_name='NM_003159.2')
        last_entry = Transcript.objects.last()
        self.assertEqual(last_entry.transcript_name, 'NM_003159.2')

    def test_add_transcript_blank(self):
        """
        Test adding empty values to the transcript model.
        :return:
        """
        Transcript.objects.get_or_create(transcript_name='')
        last_entry = Transcript.objects.last()
        self.assertEqual(last_entry.transcript_name, '')


class GenomicLocationModelCreateTests(TestCase):
    def test_add_genomic_location(self):
        """
        Test adding genomic location information to the Genomic Location model
        """
        GenomicLocation.objects.get_or_create(assembly='GRCh37', chromosome='1', start='25598276',
                                              stop='25655538', region="")

        last_genomic_loc = GenomicLocation.objects.last()
        self.assertEqual(last_genomic_loc.assembly, 'GRCh37')
        self.assertEqual(last_genomic_loc.start, '25598276')

    def test_add_genomic_location_blank(self):
        """
        Test for adding blank values to the Genomic Location model.
        :return:
        """
        GenomicLocation.objects.get_or_create(assembly='', chromosome='', start='', stop='',
                                              region='')
        last_entry = GenomicLocation.objects.last()
        self.assertEqual(last_entry.assembly, '')
        self.assertEqual(last_entry.region, '')


class MappingModelCreateTests(TestCase):
    def test_add_mappings(self):
        """
        Test for adding mappings to the mapping model.
        :return:
        """
        Mapping.objects.get_or_create(mapping_name='NM_003159.2:c.-162-?_99+?del')
        last_entry = Mapping.objects.last()
        self.assertEqual(last_entry.mapping_name, 'NM_003159.2:c.-162-?_99+?del')

    def test_add_mapping_blank(self):
        """
        Test for adding blank values to the Mapping model.
        :return:
        """
        Mapping.objects.get_or_create(mapping_name='')
        last_entry = Mapping.objects.last()
        self.assertEqual(last_entry.mapping_name, '')


class VariantModelCreateTests(TestCase):
    def test_add_variant(self):
        """
        Test for adding the variant extras to the Variant model.
        """
        ref_allele, created = Allele.objects.get_or_create(allele='G')
        alt_allele, created = Allele.objects.get_or_create(allele='A')
        reported_ref, created = Allele.objects.get_or_create(allele='G')
        reported_alt, created = Allele.objects.get_or_create(allele='A')

        self.assertEqual(ref_allele, reported_ref)
        self.assertEqual(alt_allele, reported_alt)

        Variant.objects.create(ref_allele=ref_allele, alt_allele=alt_allele, reported_ref=reported_ref,
                               reported_alt=reported_alt, protein_change='p.Pro384_Ser395delinsArg')

        last_variant = Variant.objects.last()
        self.assertEqual(last_variant.protein_change, 'p.Pro384_Ser395delinsArg')

    def test_add_variant_blank(self):
        """
        Test for adding blank values to the Variant (extras) model.
        :return:
        """
        ref_allele, created = Allele.objects.get_or_create(allele='')
        alt_allele, created = Allele.objects.get_or_create(allele='')
        reported_ref, created = Allele.objects.get_or_create(allele='')
        reported_alt, created = Allele.objects.get_or_create(allele='')

        Variant.objects.create(ref_allele=ref_allele, alt_allele=alt_allele, reported_ref=reported_ref,
                               reported_alt=reported_alt, protein_change='')
        last_entry = Variant.objects.last()
        self.assertEqual(last_entry.protein_change, '')


class SourceModelCreateTests(TestCase):
    def test_add_source(self):
        """
        Test for Source model.
        :return:
        """
        Source.objects.get_or_create(source='ClinVar', last_eval='2014-03-13', last_updated='2017-09-14',
                                     source_url='https://www.ncbi.nlm.nih.gov/clinvar/RCV000170005')
        last_entry = Source.objects.last()
        self.assertEqual(last_entry.source, 'ClinVar')
        self.assertEqual(last_entry.source_url, 'https://www.ncbi.nlm.nih.gov/clinvar/RCV000170005')

    def test_add_source_blank(self):
        Source.objects.get_or_create(source='', last_eval='', last_updated='', source_url='')
        last_entry = Source.objects.last()
        self.assertEqual(last_entry.source, '')
        self.assertEqual(last_entry.source_url, '')


class ClassificationModelCreateTests(TestCase):
    """
    Tests for the Classification Model
    """
    def test_add_classification(self):
        Classification.objects.create(name='Pathogenic')
        last_entry = Classification.objects.last()
        self.assertEqual(last_entry.name, 'Pathogenic')

    def test_add_classification_blank(self):
        Classification.objects.create(name='')
        last_entry = Classification.objects.last()
        self.assertEqual(last_entry.name, '')


class ExtraPropertiesModelCreateTests(TestCase):
    """
    Tests for the ExtraProperties model
    """
    def test_add_extra_properties_comments(self):
        ExtraProperties.objects.create(submitter_comments='The variant was identified prenatally and suggested risk '
                                                          'for Menkes disease, which did not however develop.',
                                       alias='')
        last_entry = ExtraProperties.objects.last()
        self.assertEqual(last_entry.submitter_comments, 'The variant was identified prenatally and suggested risk for '
                                                        'Menkes disease, which did not however develop.')

    def test_add_extra_properties_alias(self):
        ExtraProperties.objects.get_or_create(submitter_comments='', alias='I397SFSTER19')
        last_entry = ExtraProperties.objects.last()
        self.assertEqual(last_entry.alias, 'I397SFSTER19')

    def test_add_extra_properties_blank(self):
        ExtraProperties.objects.get_or_create(submitter_comments='', alias='')
        last_entry = ExtraProperties.objects.last()
        self.assertEqual(last_entry.alias, '')


class GeneVariantInfoCreateTests(TestCase):

    def test_gene_variant(self):
        """
        Test adding a gene variant
        :return:
        """
        gene = Gene.objects.create(gene_name='CDKL5')
        genomic_loc = GenomicLocation.objects.create(assembly='', chromosome='', start='', stop='', region='')
        transcript1 = Transcript.objects.create(transcript_name='NM_003159.2')
        mapping1 = Mapping.objects.create(mapping_name='NM_003159.2:c.-162-?_99+?del')
        ref = Allele.objects.create(allele='')
        alt = Allele.objects.create(allele='')
        rep_ref = Allele.objects.create(allele='')
        rep_alt = Allele.objects.create(allele='')
        variant_extras = Variant.objects.create(ref_allele=ref, alt_allele=alt, reported_ref=rep_ref,
                                                reported_alt=rep_alt, protein_change='')
        rep_classification = Classification.objects.create(name='Pathogenic')
        inf_classification = Classification.objects.create(name='Pathogenic')
        source = Source.objects.create(source='ClinVar', last_eval='2014-03-13', last_updated='2017-09-14',
                                       source_url='https://www.ncbi.nlm.nih.gov/clinvar/RCV000170005')
        extra_props = ExtraProperties.objects.create(submitter_comments='', alias='')

        gene_variant_info = GeneVariantInfo.objects.create(gene=gene, variant_extras=variant_extras,
                                                           genomic_location=genomic_loc, source=source,
                                                           reported_classification=rep_classification,
                                                           inferred_classification=inf_classification,
                                                           extra_properties=extra_props)
        MappingJoinTable.objects.create(mapping=mapping1, gene_variant=gene_variant_info,
                                        nucleotide_change=True)
        TranscriptJoinTable.objects.create(transcript=transcript1, gene_variant=gene_variant_info, accession=False)

        last_gene_variant = GeneVariantInfo.objects.last()
        self.assertEqual(last_gene_variant.reported_classification, rep_classification)
        self.assertEqual(last_gene_variant.gene, gene)
        self.assertEqual(last_gene_variant.genomic_location, genomic_loc)
