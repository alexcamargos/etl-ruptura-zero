#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: factory.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

import pandera.pandas as pa
from loguru import logger

from ruptura_zero.extractor.excel_extractor import ExcelExtractor
from ruptura_zero.loader.data_loader import DataLoader
from ruptura_zero.manager import PipelineManager
from ruptura_zero.pipeline import Pipeline
from ruptura_zero.protocols.data_persistence import DataPersistenceProtocol
from ruptura_zero.services.data_cleaning_service import DataCleaningService
from ruptura_zero.services.data_transforming_service import DataTransformingService
from ruptura_zero.transformer.cleaner import DataCleaner
from ruptura_zero.transformer.data_cleaning_schemas import DATA_CLEANING_SCHEMAS
from ruptura_zero.transformer.data_merge import DataMerger
from ruptura_zero.transformer.pandera_schemas import CONSOLIDATED_SCHEMA
from ruptura_zero.utilities.configurations import Config as Cfg
from ruptura_zero.utilities.data_persistence import DataPersistence


def create_cleaning_service(schema: list[dict]) -> DataCleaningService:
    """Create the data cleaning service.

    Args:
        schema (list[dict]): The schema to be used for data cleaning.

    Returns:
        DataCleaningService: The data cleaning service instance.
    """

    logger.info('Criando o serviço de limpeza de dados...')
    cleaner = DataCleaner()

    return DataCleaningService(cleaner, schema)


def create_transforming_service(data_persister: DataPersistenceProtocol,
                                schema: pa.DataFrameSchema) -> DataTransformingService:
    """Create the data transforming service.

    Args:
        schema (pa.DataFrameSchema): The schema to be used for data transforming.

    Returns:
        DataTransformingService: The data transforming service instance.
    """

    logger.info('Criando o serviço de transformação de dados...')
    merger = DataMerger()

    return DataTransformingService(merger, data_persister, schema)


def build_application():
    """Build the ETL application."""

    logger.info('Construindo a aplicação ETL...')

    # Create an ExcelExtractor instance.
    logger.info('Criando o extrator Excel...')
    extractor = ExcelExtractor(Cfg.RAW_DATA.value / Cfg.RAW_DATA_FILE.value)

    # Criando o serviço de limpeza de dados.
    cleaning_service = create_cleaning_service(DATA_CLEANING_SCHEMAS)

    # Create a DataPersistence instance.
    logger.info('Criando o persistente de dados...')
    data_persistence = DataPersistence()

    # Criando o serviço de transformação de dados.
    transforming_service = create_transforming_service(data_persistence, CONSOLIDATED_SCHEMA)

    # Create a DataLoader instance.
    logger.info('Criando o carregador de dados...')
    loader = DataLoader()

    # Create a Pipeline instance.
    logger.info('Criando o pipeline...')
    pipeline = Pipeline(extractor,
                        cleaning_service,
                        transforming_service,
                        loader)

    return PipelineManager(pipeline)
