import json

from django.test import TestCase
from rest_framework.test import RequestsClient


class GeneViewSetTests(TestCase):
    # Initial Fixture has data for 101 different variants with some genes having multiple variants.
    fixtures = ['variants/fixtures/initial_data.json']

    def test_gene_filtering(self):
        """
        API test for finding genes.
        :return:
        """
        client = RequestsClient()

        response = client.get('http://127.0.0.1:8000/api/M')
        self.assertTrue(response.status_code == 200)

        response_json = json.loads(response.text)
        self.assertEqual(response_json['count'], 7)

        response = client.get('http://127.0.0.1:8000/api/ME')
        response_json = json.loads(response.text)
        self.assertEqual(response_json['count'], 2)

        response = client.get('http://127.0.0.1:8000/api/MS')
        response_json = json.loads(response.text)
        self.assertEqual(response_json['count'], 2)

        response = client.get('http://127.0.0.1:8000/api/MEC')
        response_json = json.loads(response.text)
        self.assertEqual(response_json['count'], 1)


class GeneVariantInfoViewSetTests(TestCase):
    fixtures = ['variants/fixtures/initial_data.json']

    def test_gene_variant_info_by_gene(self):
        """
        API test to check variants for a gene.
        :return:
        """
        client = RequestsClient()

        # Gene with multiple variants (not ordered)
        response = client.get('http://127.0.0.1:8000/api/variants/TSC1')
        response_json = json.loads(response.text)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(response_json['count'], 11)

        # Gene with only one variant
        response = client.get('http://127.0.0.1:8000/api/variants/BBS1')
        response_json = json.loads(response.text)
        self.assertEqual(response_json['count'], 1)

        # Some checks for content
        single_result = response_json['results'][0]
        gene_name = single_result['gene']['gene_name']
        self.assertEqual(gene_name, 'BBS1')

        transcripts = single_result['transcripts']
        self.assertEqual(len(transcripts), 4)

