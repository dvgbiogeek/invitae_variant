from __future__ import division, print_function, unicode_literals, absolute_import

import io
import logging
import os
import zipfile

from csv import DictReader

from variants.data_importer import VariantImporter


def run(*script_args):
    """
    Script for importing variant data. Data file should be zipped. Can be run as a manage command:
    python manage.py runscript import_variants --script-args=variants/scripts/data/variants.tsv.zip
    :param script_args:
    :return:
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
    logger = logging.getLogger("variants.import_variants")

    zipped_tsv_file = os.path.expanduser(*script_args)

    # Setup file for failed imports
    output_dir = './variants/scripts/output'
    os.makedirs(output_dir, exist_ok=True)
    error_list_path = os.path.join(output_dir, "import_errors.txt")
    with io.open(error_list_path, 'wt') as err_list_out:
        err_list_out.write("")

    with zipfile.ZipFile(zipped_tsv_file) as zipped_file:
        filelist = zipped_file.filelist
        for zfile in filelist:
            with zipped_file.open(zfile.filename) as open_zip:
                zip_in_text = io.TextIOWrapper(open_zip)
                reader = DictReader(zip_in_text, dialect='excel-tab')

                read_as_list = list(reader)
                logger.info("Found {} entries.".format(len(read_as_list)))
                variants_read = 0
                variants_imported = 0
                errors = 0

                for row in read_as_list:
                    logger.info("Variant {}".format(variants_read))
                    variants_read += 1
                    try:
                        importer = VariantImporter()
                        variant = importer.import_variant(row)
                        logger.info("Loaded variant {} {} {}".format(variants_read, row['Gene'], row['Nucleotide Change']))
                        variants_imported += 1
                    except Exception as e:
                        errors += 1
                        logger.error("Row {} with data {} did not import.".format(variants_read, row))
                        logger.error(e)
                        with io.open(error_list_path, 'at', encoding='utf-8') as f:
                            f.write("{} {} - {}\n".format(variants_read, row, e))

                logger.info("Variants read: {}".format(variants_read))
                logger.info("Variants imported: {}".format(variants_imported))
                logger.info("Variants with errors: {}".format(errors))
