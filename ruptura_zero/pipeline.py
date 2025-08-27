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

from loguru import logger

from ruptura_zero.extractor.excel_extractor import ExcelExtractor
from ruptura_zero.transformer.cleaner import DataCleaner
from ruptura_zero.transformer.data_cleaning_schemas import DATA_CLEANING_SCHEMAS


class Pipeline:
    """Defines the ETL pipeline for the Ruptura Zero project."""

    def __init__(self, extractor: ExcelExtractor, cleaner: DataCleaner) -> None:
        """Initialize the Pipeline."""

        logger.info('Inicializando o Pipeline...')

        # Set the extractor.
        self.extractor = extractor

        # Set the cleaner.
        self.cleaner = cleaner

        # Initialize data attributes.
        self.ruptura_data = None
        self.vendas_data = None
        self.estoque_data = None

    def extract_from_source(self) -> None:
        """Extract data from the source."""

        logger.info('Extraindo dados da fonte...')

        sheets = self.extractor.extract()

        self.ruptura_data = sheets.get('01_BD_Ruptura')
        self.vendas_data = sheets.get('02_BD_Estoque')
        self.estoque_data = sheets.get('03_BD_Vendas')

        if (self.ruptura_data is None or
                self.vendas_data is None or
                self.estoque_data is None):
            logger.error('Erro ao extrair os dados. Verifique as planilhas e tente novamente.')

    def clean_and_validate_data(self) -> None:
        """Clean and validate the data."""

        logger.info('Limpando e validando todos os conjuntos de dados...')

        for schema in DATA_CLEANING_SCHEMAS:
            # Obtendo o DataFrame correspondente ao esquema.
            data_frame = getattr(self, schema['data_attr'])
            if data_frame is not None:
                logger.info(f'Limpando dados de {schema["name"].lower()}...')
                # Aplicando a limpeza de dados.
                cleaned_dataframe = self.cleaner.clean(data_frame, schema['types'])
                # Atribuindo o DataFrame limpo de volta ao atributo da classe.
                setattr(self, schema['data_attr'], cleaned_dataframe)
            else:
                logger.error(f'Dados de {schema["name"].lower()} não foram extraídos corretamente.')

    def transform_for_analysis(self) -> None:
        """Transform the data for analysis."""

        logger.info('Transformando dados para análise...')

    def load_to_destination(self) -> None:
        """Load the data into the destination."""

        logger.info('Carregando dados para o destino...')
