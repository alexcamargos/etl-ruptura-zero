#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: pipeline.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from typing import Mapping

import pandas as pd
from loguru import logger

from ruptura_zero.protocols.extractor import ExtractorProtocol
from ruptura_zero.protocols.loader import LoaderProtocol
from ruptura_zero.protocols.transformer import (DataCleaningServiceProtocol,
                                                DataTransformingServiceProtocol)
from ruptura_zero.utilities.configurations import Config as Cfg


class Pipeline:
    """Defines the ETL pipeline for the Ruptura Zero project."""

    def __init__(self,
                 extractor: ExtractorProtocol,
                 cleaning_service: DataCleaningServiceProtocol,
                 transforming_service: DataTransformingServiceProtocol,
                 loader: LoaderProtocol) -> None:
        """Initialize the Pipeline.

        Args:
            extractor (ExcelExtractor): The extractor instance.
            cleaning_service (DataCleaningService): The cleaning service instance.
            merger (DataMerger): The merger instance.
            loader (DataLoader): The loader instance.
            data_persistence (DataPersistence): The data persistence instance.
        """

        logger.info('Inicializando o Pipeline...')

        # Set the extractor.
        self.extractor = extractor

        # Set the cleaning service.
        self.cleaning_service = cleaning_service

        # Set the transformation service.
        self.transforming_service = transforming_service

        # Set the loader.
        self.loader = loader

    def extract_from_source(self) -> Mapping[str, pd.DataFrame | None]:
        """Extract data from the source."""

        logger.info('Extraindo os dados brutos do Excel...')

        sheets = self.extractor.extract()

        extract_data = {'ruptura_data': sheets.get(Cfg.SHEET_RUPTURA.value),
                        'estoque_data': sheets.get(Cfg.SHEET_ESTOQUE.value),
                        'vendas_data': sheets.get(Cfg.SHEET_VENDAS.value)}

        return extract_data

    def clean_and_validate_data(self,
                                extracted_data: Mapping[str,
                                                        pd.DataFrame | None]
                                ) -> Mapping[str, pd.DataFrame | None]:
        """Clean and validate the data."""

        logger.info('Limpando e validando todos os conjuntos de dados...')

        return self.cleaning_service.run(extracted_data)

    def transform_for_analysis(self, cleaned_data: Mapping[str, pd.DataFrame | None]) -> pd.DataFrame | None:
        """Transform the data for analysis."""

        logger.info('Transformando os dados para análise...')

        return self.transforming_service.run(cleaned_data)

    def load_to_destination(self, final_data: pd.DataFrame | None) -> None:
        """Load the data into the destination."""

        logger.info('Carregando os dados para o MotherDuck...')

        if final_data is not None:
            # Carregando os dados consolidados para o MotherDuck.
            self.loader.load_data(final_data, to_motherduck=True)
        else:
            logger.warning('Nenhum dado final para carregar no MotherDuck.')
