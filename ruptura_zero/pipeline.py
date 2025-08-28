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
from pandera.errors import SchemaError

from ruptura_zero.extractor.excel_extractor import ExcelExtractor
from ruptura_zero.transformer.cleaner import DataCleaner
from ruptura_zero.transformer.data_cleaning_schemas import DATA_CLEANING_SCHEMAS
from ruptura_zero.transformer.data_merge import DataMerger


class Pipeline:
    """Defines the ETL pipeline for the Ruptura Zero project."""

    def __init__(self, extractor: ExcelExtractor, cleaner: DataCleaner, merger: DataMerger) -> None:
        """Initialize the Pipeline."""

        logger.info('Inicializando o Pipeline...')

        # Set the extractor.
        self.extractor = extractor

        # Set the cleaner.
        self.cleaner = cleaner

        # Set the merger.
        self.merger = merger

        # Initialize data attributes.
        self.ruptura_data = None
        self.vendas_data = None
        self.estoque_data = None
        self.ruptura_estoque_data = None
        self.ruptura_estoque_vendas_data = None

    def extract_from_source(self) -> None:
        """Extract data from the source."""

        logger.info('Extraindo os dados brutos do Excel...')

        sheets = self.extractor.extract()

        self.ruptura_data = sheets.get('01_BD_Ruptura')
        self.estoque_data = sheets.get('02_BD_Estoque')
        self.vendas_data = sheets.get('03_BD_Vendas')

    def clean_and_validate_data(self) -> None:
        """Clean and validate the data."""

        logger.info('Limpando e validando todos os conjuntos de dados...')

        for data_cleaning_schema in DATA_CLEANING_SCHEMAS:
            # Obtendo o DataFrame correspondente ao esquema.
            data_frame = getattr(self, data_cleaning_schema['data_attr'])

            if data_frame is not None:
                # Renomear colunas com base no esquema.
                columns_mapping = data_cleaning_schema.get('columns')
                if columns_mapping:
                    logger.info(f'Renomeando colunas de {data_cleaning_schema["name"]}...')
                    data_frame = data_frame.rename(columns=columns_mapping)

                # Aplicando a limpeza de dados.
                logger.info(f'Limpando dados de {data_cleaning_schema["name"]}...')
                cleaned_dataframe = self.cleaner.clean(data_frame, data_cleaning_schema['types'])

                # Validação de dados com Pandera.
                pandera_schema = data_cleaning_schema.get('pandera_schema')
                if not pandera_schema:
                    logger.warning(
                        f'Nenhum esquema Pandera encontrado para {data_cleaning_schema["name"]}. Pulando a validação.')
                else:
                    try:
                        logger.info(f'Validando dados de {data_cleaning_schema["name"]} com Pandera...')
                        pandera_schema.validate(cleaned_dataframe, lazy=True)
                        logger.success(f'Validação de {data_cleaning_schema["name"]} bem-sucedida.')
                    except SchemaError as error:
                        logger.error(f'Validação de dados para {data_cleaning_schema["name"]} falhou.')
                        logger.error(f'Causa do erro:\n{error.failure_cases}')

                        raise error

                # Atribuindo o DataFrame limpo de volta ao atributo da classe.
                setattr(self, data_cleaning_schema['data_attr'], cleaned_dataframe)
            else:
                logger.error(
                    f'Dados de {data_cleaning_schema["name"].lower()} não foram extraídos corretamente.')

    def transform_for_analysis(self) -> None:
        """Transform the data for analysis."""

        logger.info('Transformando os dados para análise...')

        # Consolida os dados de ruptura e estoque.
        ruptura_estoque_merged = self.merger.merge_data(data_frame_left=self.ruptura_data,
                                                        data_frame_right=self.estoque_data,
                                                        left_key=['mes', 'cliente_id', 'categoria_material'],
                                                        right_key=['mes', 'cliente_id', 'categoria_material'],
                                                        how='inner',
                                                        suffixes=('_ruptura', '_estoque'))
        self.ruptura_estoque_data = ruptura_estoque_merged

        # Consolida os dados de ruptura, estoque e vendas.
        ruptura_estoque_vendas = self.merger.merge_data(data_frame_left=ruptura_estoque_merged,
                                                        data_frame_right=self.vendas_data,
                                                        left_key=['mes', 'cliente_id'],
                                                        right_key=['mes', 'cliente_id'],
                                                        how='inner',
                                                        suffixes=('_ruptura_estoque', '_vendas'))
        self.ruptura_estoque_vendas_data = ruptura_estoque_vendas

    def load_to_destination(self) -> None:
        """Load the data into the destination."""

        logger.info('Carregando os dados para o destino...')
