from django.test import TestCase

from variants.models import Gene, Transcript, GenomicLocation, OtherMappings, Variant, Source, Classification, \
    ExtraProperties, GeneVariantInfo


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
        Transcript.objects.get_or_create(transcript='NM_003159.2')
        last_entry = Transcript.objects.last()
        self.assertEqual(last_entry.transcript, 'NM_003159.2')

    def test_add_transcript_blank(self):
        Transcript.objects.get_or_create(transcript='')
        last_entry = Transcript.objects.last()
        self.assertEqual(last_entry.transcript, '')


class GenomicLocationModelCreateTests(TestCase):
    def test_add_genomic_location(self):
        GenomicLocation.objects.get_or_create(assembly='GRCh37', chromosome='1', start='25598276', stop='25655538',
                                              accession='NC_000001.10')
        last_entry = GenomicLocation.objects.last()
        self.assertEqual(last_entry.assembly, 'GRCh37')
        self.assertEqual(last_entry.accession, 'NC_000001.10')

    def test_add_genomic_location_blank(self):
        GenomicLocation.objects.get_or_create(assembly='', chromosome='', start='', stop='',
                                              accession='')
        last_entry = GenomicLocation.objects.last()
        self.assertEqual(last_entry.assembly, '')
        self.assertEqual(last_entry.accession, '')

    def test_add_genomic_location_blank_accession(self):
        GenomicLocation.objects.get_or_create(assembly='GRCh37', chromosome='1', start='25598276', stop='25655538',
                                              accession='')
        last_entry = GenomicLocation.objects.last()
        self.assertEqual(last_entry.assembly, 'GRCh37')
        self.assertEqual(last_entry.accession, '')


class OtherMappingsModelCreateTests(TestCase):
    def test_add_other_mappings(self):
        OtherMappings.objects.get_or_create(other_mapping='NM_003159.2:c.-162-?_99+?del')
        last_entry = OtherMappings.objects.last()
        self.assertEqual(last_entry.other_mapping, 'NM_003159.2:c.-162-?_99+?del')

    def test_add_other_mapping_blank(self):
        OtherMappings.objects.get_or_create(other_mapping='')
        last_entry = OtherMappings.objects.last()
        self.assertEqual(last_entry.other_mapping, '')


class VariantModelCreateTests(TestCase):
    def test_add_variant(self):
        Variant.objects.get_or_create(nucleotide_change='NM_006493.2:c.835G>A', protein_change='p.Asp279Asn',
                                      ref_allele='G', alt_allele='A', reported_ref='G', reported_alt='A')
        last_entry = Variant.objects.last()
        self.assertEqual(last_entry.nucleotide_change, 'NM_006493.2:c.835G>A')
        self.assertEqual(last_entry.protein_change, 'p.Asp279Asn')

    def test_add_variant_blank(self):
        Variant.objects.get_or_create(nucleotide_change='', protein_change='', ref_allele='', alt_allele='',
                                      reported_ref='', reported_alt='')
        last_entry = Variant.objects.last()
        self.assertEqual(last_entry.nucleotide_change, '')
        self.assertEqual(last_entry.protein_change, '')

    def test_add_variant_blank_ref_alt(self):
        Variant.objects.get_or_create(nucleotide_change='NM_000093.4:c.3259_3366del',
                                      protein_change='p.Ser1088_Gly1123del', ref_allele='', alt_allele='',
                                      reported_ref='', reported_alt='')
        last_entry = Variant.objects.last()
        self.assertEqual(last_entry.nucleotide_change, 'NM_000093.4:c.3259_3366del')
        self.assertEqual(last_entry.ref_allele, '')


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
        Classification.objects.get_or_create(reported='Pathogenic', inferred='Pathogenic')
        last_entry = Classification.objects.last()
        self.assertEqual(last_entry.reported, 'Pathogenic')

    def test_add_classification_blank(self):
        Classification.objects.get_or_create(reported='', inferred='')
        last_entry = Classification.objects.last()
        self.assertEqual(last_entry.reported, '')


class ExtraPropertiesModelCreateTests(TestCase):
    def test_add_extra_properties_comments(self):
        ExtraProperties.objects.get_or_create(submitter_comments='The variant was identified prenatally and suggested '
                                                                 'risk for Menkes disease, which did not however '
                                                                 'develop.',
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