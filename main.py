#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: main.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from loguru import logger

from ruptura_zero.extractor.excel_extractor import ExcelExtractor
from ruptura_zero.manager import PipelineManager
from ruptura_zero.pipeline import Pipeline
from ruptura_zero.transformer.cleaner import DataCleaner
from ruptura_zero.transformer.data_merge import DataMerger
from ruptura_zero.utilities.configurations import Config as Cfg
from ruptura_zero.utilities.data_persistence import DataPersistence


def main(pipeline_manager: PipelineManager) -> None:
    """Run the main ETL pipeline.

    This function orchestrates the ETL process by calling the appropriate methods
    on the PipelineManager instance.

    Args:
        pipeline_manager (PipelineManager): The pipeline manager instance.
    """

    # Data extraction.
    pipeline_manager.extractor()

    # Data cleaning and validation.
    pipeline_manager.cleaner()

    # Data transformation.
    pipeline_manager.transformer()

    # Data loading.
    pipeline_manager.loader()


if __name__ == "__main__":
    # Starting the ETL process.
    logger.info('Ruptura Zero: Análise de Vendas e Estoques...')
    logger.info('Iniciando o processo ETL...')

    # Create an ExcelExtractor instance.
    extractor = ExcelExtractor(Cfg.RAW_DATA.value / 'ruptura_database.xlsx')

    # Create a DataCleaner instance.
    cleaner = DataCleaner()

    # Create a DataMerger instance.
    merger = DataMerger()

    # Create a DataPersistence instance.
    data_persistence = DataPersistence()

    # Create a Pipeline instance.
    pipeline = Pipeline(extractor, cleaner, merger, data_persistence)

    # Create a PipelineManager instance.
    pipeline_manager = PipelineManager(pipeline)

    # Run the main function.
    main(pipeline_manager)
