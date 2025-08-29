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

from loguru import logger

from ruptura_zero.extractor.excel_extractor import ExcelExtractor
from ruptura_zero.loader.data_loader import DataLoader
from ruptura_zero.manager import PipelineManager
from ruptura_zero.pipeline import Pipeline
from ruptura_zero.services.data_cleaning_service import DataCleaningService
from ruptura_zero.transformer.cleaner import DataCleaner
from ruptura_zero.transformer.data_cleaning_schemas import DATA_CLEANING_SCHEMAS
from ruptura_zero.transformer.data_merge import DataMerger
from ruptura_zero.utilities.configurations import Config as Cfg
from ruptura_zero.utilities.data_persistence import DataPersistence


def build_application():
    """Build the ETL application."""

    logger.info('Construindo a aplicação ETL...')

    # Create an ExcelExtractor instance.
    logger.info('Criando o extrator Excel...')
    extractor = ExcelExtractor(Cfg.RAW_DATA.value / Cfg.RAW_DATA_FILE.value)

    # Criando a DataCleaner instance.
    logger.info('Criando a DataCleaner...')
    cleaner = DataCleaner()

    # Criando o serviço de limpeza de dados.
    logger.info('Criando o serviço de limpeza de dados...')
    cleaning_service = DataCleaningService(cleaner, DATA_CLEANING_SCHEMAS)

    # Create a DataMerger instance.
    logger.info('Criando o consolidador de dados...')
    merger = DataMerger()

    # Create a DataLoader instance.
    logger.info('Criando o carregador de dados...')
    loader = DataLoader()

    # Create a DataPersistence instance.
    logger.info('Criando o persistente de dados...')
    data_persistence = DataPersistence()

    # Create a Pipeline instance.
    logger.info('Criando o pipeline...')
    pipeline = Pipeline(extractor,
                        cleaning_service,
                        merger,
                        loader,
                        data_persistence)

    return PipelineManager(pipeline)
