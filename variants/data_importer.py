from variants.models import Gene, Transcript, GenomicLocation, TranscriptJoinTable, Allele, Mapping, MappingJoinTable, \
    Source, ExtraProperties, Variant, Classification, GeneVariantInfo


class VariantImporter(object):
    def import_variant(self, tsv_row):
        # attempt to normalize empty and Null values to be acceptable for model with CharFields
        for k, v in tsv_row.items():
            if v is None or v == 'NULL':
                tsv_row[k] = ''

        # Add Gene
        gene_name = tsv_row.get('Gene', '')
        gene, created = Gene.objects.get_or_create(gene_name=gene_name)

        # Add Genomic Location and Transcripts
        genomic_location = self.genomic_location_for_variant(tsv_row)
        transcripts = self.transcripts_for_variant(tsv_row)
        accession = tsv_row.get('Accession', '')
        self.add_transcripts_to_genomic_location(genomic_location, transcripts, accession)

        # Add Variant and Mappings
        variant = self.variant(tsv_row)
        mappings = self.mapping(tsv_row)
        nucleotide_change = tsv_row.get('Nucleotide Change', '')
        self.add_mappings_to_variant(variant, mappings, nucleotide_change)

        # Add Source
        source = self.source_for_variant(tsv_row)

        # Add Classification
        reported_classification = self.classification_for_variant(tsv_row, 'Reported Classification')
        inferred_classification = self.classification_for_variant(tsv_row, 'Inferred Classification')

        # Add Extra Properties
        extra_properties = self.extra_properties_for_variant(tsv_row)

        # Connect all the objects into a GeneVariantInfo object
        add_variant, created = GeneVariantInfo.objects.get_or_create(gene=gene, variant=variant,
                                                                     genomic_location=genomic_location, source=source,
                                                                     reported_classification=reported_classification,
                                                                     inferred_classification=inferred_classification,
                                                                     extra_properties=extra_properties)
        print(created)
        return add_variant

    def transcripts_for_variant(self, tsv_row):
        transcripts = list_of_items_by_key(tsv_row, 'Transcripts')
        list_of_transcripts = []
        for transcript in transcripts:
            transcript, created = Transcript.objects.get_or_create(name=transcript)
            list_of_transcripts.append(transcript)
        return list_of_transcripts

    def genomic_location_for_variant(self, tsv_row):
        assembly = tsv_row.get('Assembly', '')
        chromosome = tsv_row.get('Chr', '')
        genome_start = tsv_row.get('Genomic Start', '')
        genome_end = tsv_row.get('Genomic Stop', '')
        region = tsv_row.get('Region', '')

        genomic_location = GenomicLocation.objects.create(assembly=assembly, chromosome=chromosome, start=genome_start,
                                                          stop=genome_end, region=region)
        return genomic_location

    def add_transcripts_to_genomic_location(self, genomic_location, transcripts, accession):
        for transcript in transcripts:
            is_accession = accession != '' and transcript.name == accession
            TranscriptJoinTable.objects.get_or_create(transcript=transcript, genomic_location=genomic_location,
                                                      accession=is_accession)

    def source_for_variant(self, tsv_row):
        source = tsv_row.get('Source', '')
        last_eval = tsv_row.get('Last Evaluated', '')
        last_updated = tsv_row.get('Last Updated', '')
        url = tsv_row.get('URL', '')

        source, created = Source.objects.get_or_create(source=source, last_eval=last_eval, last_updated=last_updated,
                                                       source_url=url)
        return source

    def extra_properties_for_variant(self, tsv_row):
        submitter_comments = tsv_row.get('Submitter Comment', '')
        alias = tsv_row.get('Alias', '')

        extra_properties, created = ExtraProperties.objects.get_or_create(submitter_comments=submitter_comments,
                                                                          alias=alias)
        return extra_properties

    def variant(self, tsv_row):
        ref_allele = tsv_row.get('Ref')
        alt_allele = tsv_row.get('Alt')
        rep_ref = tsv_row.get('Reported Ref')
        rep_alt = tsv_row.get('Reported Alt')

        ref, created = Allele.objects.get_or_create(allele=ref_allele)
        alt, created = Allele.objects.get_or_create(allele=alt_allele)
        reported_ref, created = Allele.objects.get_or_create(allele=rep_ref)
        reported_alt, created = Allele.objects.get_or_create(allele=rep_alt)

        protein_change = tsv_row.get('Protein Change', '')

        variant = Variant.objects.create(ref_allele=ref, alt_allele=alt, reported_ref=reported_ref,
                                         reported_alt=reported_alt,  protein_change=protein_change)

        return variant

    def mapping(self, tsv_row):
        mappings = list_of_items_by_key(tsv_row, 'Other Mappings')
        list_of_mappings = []
        for mapping in mappings:
            mapping, created = Mapping.objects.get_or_create(name=mapping)
            list_of_mappings.append(mapping)
        return list_of_mappings

    def add_mappings_to_variant(self, variant, mappings, nucleotide_change):
        for mapping in mappings:
            is_nucleotide_change = nucleotide_change is not '' and mapping.name == nucleotide_change
            MappingJoinTable.objects.get_or_create(mapping=mapping, variant=variant,
                                                   nucleotide_change=is_nucleotide_change)

    def classification_for_variant(self, tsv_row, key):
        classification_value = tsv_row.get(key, '')
        classification, created = Classification.objects.get_or_create(name=classification_value)
        return classification


def list_of_items_by_key(tsv_row, key):
    items = tsv_row.get(key, '')
    if items:
        items = items.split(',')
    return items
