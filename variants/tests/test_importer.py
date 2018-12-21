from django.test import TestCase

from variants.data_importer import VariantImporter
from variants.models import GeneVariantInfo


class DataImportFunctionalTests(TestCase):
    def data_variant_with_None(self):
        variant = {'Other Mappings': 'NM_003159.2:c.-162-?_99+?del', 'Accession': None, 'Transcripts': 'NM_003159.2',
                   'Reported Ref': None, 'Reported Classification': 'Pathogenic',
                   'Inferred Classification': 'Pathogenic', 'Last Updated': '2017-09-14', 'Assembly': None,
                   'Source': 'ClinVar', 'URL': 'https://www.ncbi.nlm.nih.gov/clinvar/RCV000170005',
                   'Protein Change': '', 'Ref': None, 'Genomic Stop': None, 'Last Evaluated': '2014-03-13',
                   'Alias': '', 'Region': '', 'Chr': None, 'Nucleotide Change': 'NM_003159.2:c.-162-?_99+?del',
                   'Alt': None, 'Reported Alt': None, 'Gene': 'CDKL5', 'Genomic Start': None, 'Submitter Comment': ''}
        return variant

    def data_variant(self):
        variant = {'Other Mappings': 'NM_003159.2:c.-162-?_99+?del', 'Accession': '', 'Transcripts': 'NM_003159.2',
                   'Reported Ref': '', 'Reported Classification': 'Pathogenic', 'Inferred Classification': 'Pathogenic',
                   'Last Updated': '2017-09-14', 'Assembly': '', 'Source': 'ClinVar',
                   'URL': 'https://www.ncbi.nlm.nih.gov/clinvar/RCV000170005', 'Protein Change': '', 'Ref': '',
                   'Genomic Stop': '', 'Last Evaluated': '2014-03-13', 'Alias': '', 'Region': '', 'Chr': '',
                   'Nucleotide Change': 'NM_003159.2:c.-162-?_99+?del', 'Alt': '', 'Reported Alt': '', 'Gene': 'CDKL5',
                   'Genomic Start': '', 'Submitter Comment': ''}
        return variant

    def test_import_variant1_with_None_values(self):
        importer = VariantImporter()
        data_row = self.data_variant_with_None()

        imported_variant = importer.import_variant(data_row)
        last_variant = GeneVariantInfo.objects.last()
        self.assertEqual(imported_variant, last_variant)

    def test_import_variant1(self):
        importer = VariantImporter()
        data_row = self.data_variant()

        imported_variant = importer.import_variant(data_row)
        last_variant = GeneVariantInfo.objects.last()
        self.assertEqual(imported_variant, last_variant)
