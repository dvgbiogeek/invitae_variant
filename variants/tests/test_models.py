import unittest
from django.test import TestCase

from variants.models import Gene, Transcript, Allele, GenomicLocation, Mapping, Variant, Source, Classification, \
    ExtraProperties, GeneVariantInfo, MappingJoinTable, TranscriptJoinTable


class GeneModelCreateTests(TestCase):
    def test_add_gene(self):
        Gene.objects.get_or_create(gene_name='CDKL5')
        last_entry = Gene.objects.last()
        self.assertEqual(last_entry.gene_name, 'CDKL5')

    def test_add_gene_blank(self):
        Gene.objects.get_or_create(gene_name='')
        last_entry = Gene.objects.last()
        self.assertEqual(last_entry.gene_name, '')


class TranscriptModelCreateTests(TestCase):
    def test_add_transcript(self):
        Transcript.objects.get_or_create(name='NM_003159.2')
        last_entry = Transcript.objects.last()
        self.assertEqual(last_entry.name, 'NM_003159.2')

    def test_add_transcript_blank(self):
        Transcript.objects.get_or_create(name='')
        last_entry = Transcript.objects.last()
        self.assertEqual(last_entry.name, '')


class GenomicLocationModelCreateTests(TestCase):
    def test_add_genomic_location(self):
        """
        CM000663.1, \
        NC_000001.11, \
        NC_000001.10
        """
        transcript1, created = Transcript.objects.get_or_create(name='CM000663.1')
        transcript2, created = Transcript.objects.get_or_create(name='NC_000001.11')
        transcript3, created = Transcript.objects.get_or_create(name='NC_000001.10')

        genome_loc, created = GenomicLocation.objects.get_or_create(assembly='GRCh37', chromosome='1', start='25598276',
                                                                    stop='25655538', region="")

        last_genomic_loc = GenomicLocation.objects.last()
        self.assertEqual(last_genomic_loc.assembly, 'GRCh37')
        self.assertEqual(last_genomic_loc.start, '25598276')

        TranscriptJoinTable.objects.get_or_create(transcript=transcript1, genomic_location=genome_loc,
                                                  accession=False)
        TranscriptJoinTable.objects.get_or_create(transcript=transcript2, genomic_location=genome_loc,
                                                  accession=True)
        TranscriptJoinTable.objects.get_or_create(transcript=transcript3, genomic_location=genome_loc,
                                                  accession=False)
        transcripts_for_genomic_loc = TranscriptJoinTable.objects.filter(genomic_location__genomic_location_id=
                                                                         genome_loc.genomic_location_id)
        self.assertEqual(len(transcripts_for_genomic_loc), 3)
        self.assertEqual(transcripts_for_genomic_loc[0].transcript.name, 'CM000663.1')

    def test_add_genomic_location_blank(self):
        GenomicLocation.objects.get_or_create(assembly='', chromosome='', start='', stop='',
                                              region='')
        last_entry = GenomicLocation.objects.last()
        self.assertEqual(last_entry.assembly, '')
        self.assertEqual(last_entry.region, '')


class MappingModelCreateTests(TestCase):
    def test_add_mappings(self):
        Mapping.objects.get_or_create(name='NM_003159.2:c.-162-?_99+?del')
        last_entry = Mapping.objects.last()
        self.assertEqual(last_entry.name, 'NM_003159.2:c.-162-?_99+?del')

    def test_add_mapping_blank(self):
        Mapping.objects.get_or_create(name='')
        last_entry = Mapping.objects.last()
        self.assertEqual(last_entry.name, '')


class VariantModelCreateTests(TestCase):
    def test_add_variant(self):
        """
        AJ132917.1: c.1151_1183del33, \
        NM_004992.3: c.1151_1183del33, \
        NM_001110792.1: c.1187_1219del33, \
        """
        mapping1 = Mapping.objects.create(name='AJ132917.1: c.1151_1183del33')
        mapping2 = Mapping.objects.create(name='NM_004992.3: c.1151_1183del33')
        mapping3 = Mapping.objects.create(name='NM_001110792.1: c.1187_1219del33')

        ref_allele, created = Allele.objects.get_or_create(allele='G')
        alt_allele, created = Allele.objects.get_or_create(allele='A')
        reported_ref, created = Allele.objects.get_or_create(allele='G')
        reported_alt, created = Allele.objects.get_or_create(allele='A')

        self.assertEqual(ref_allele, reported_ref)
        self.assertEqual(alt_allele, reported_alt)

        variant = Variant.objects.create(ref_allele=ref_allele, alt_allele=alt_allele, reported_ref=reported_ref,
                                         reported_alt=reported_alt, protein_change='p.Pro384_Ser395delinsArg')

        MappingJoinTable.objects.get_or_create(mapping=mapping1, variant=variant, nucleotide_change=False)
        MappingJoinTable.objects.get_or_create(mapping=mapping2, variant=variant, nucleotide_change=True)
        MappingJoinTable.objects.get_or_create(mapping=mapping3, variant=variant, nucleotide_change=False)

        last_variant = Variant.objects.last()
        self.assertEqual(last_variant.protein_change, 'p.Pro384_Ser395delinsArg')

        variant_mapping = MappingJoinTable.objects.filter(variant__variant_id=variant.variant_id)
        self.assertEqual(len(variant_mapping), 3)
        self.assertTrue(variant_mapping[1].nucleotide_change)
        self.assertEqual(variant_mapping[2].mapping.name, 'NM_001110792.1: c.1187_1219del33')

    def test_add_variant_blank(self):
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
    def test_add_classification(self):
        Classification.objects.create(name='Pathogenic')
        last_entry = Classification.objects.last()
        self.assertEqual(last_entry.name, 'Pathogenic')

    def test_add_classification_blank(self):
        Classification.objects.create(name='')
        last_entry = Classification.objects.last()
        self.assertEqual(last_entry.name, '')


class ExtraPropertiesModelCreateTests(TestCase):
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

# TODO: setup test case for join table