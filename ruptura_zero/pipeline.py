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
from pandera.errors import SchemaError

from ruptura_zero.protocols.data_persistence import DataPersistenceProtocol
from ruptura_zero.protocols.extractor import ExtractorProtocol
from ruptura_zero.protocols.loader import LoaderProtocol
from ruptura_zero.protocols.transformer import (DataCleanerProtocol,
                                                DataMergerProtocol)
from ruptura_zero.transformer.data_cleaning_schemas import DATA_CLEANING_SCHEMAS
from ruptura_zero.transformer.pandera_schemas import CONSOLIDATED_SCHEMA
from ruptura_zero.utilities.configurations import Config as Cfg
from ruptura_zero.utilities.merge_how_options import MergeHowOptions


class Pipeline:
    """Defines the ETL pipeline for the Ruptura Zero project."""

    def __init__(self,
                 extractor: ExtractorProtocol,
                 cleaner: DataCleanerProtocol,
                 merger: DataMergerProtocol,
                 loader: LoaderProtocol,
                 data_persistence: DataPersistenceProtocol) -> None:
        """Initialize the Pipeline.

        Args:
            extractor (ExcelExtractor): The extractor instance.
            cleaner (DataCleaner): The cleaner instance.
            merger (DataMerger): The merger instance.
            loader (DataLoader): The loader instance.
            data_persistence (DataPersistence): The data persistence instance.
        """

        logger.info('Inicializando o Pipeline...')

        # Set the data persistence.
        self.data_persistence = data_persistence

        # Set the extractor.
        self.extractor = extractor

        # Set the cleaner.
        self.cleaner = cleaner

        # Set the merger.
        self.merger = merger

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
                                extracted_data: Mapping[str, pd.DataFrame | None]
                                ) -> Mapping[str, pd.DataFrame | None]:
        """Clean and validate the data."""

        logger.info('Limpando e validando todos os conjuntos de dados...')

        cleaned_data = {}
        for data_cleaning_schema in DATA_CLEANING_SCHEMAS:
            # Obtendo o DataFrame correspondente ao esquema.
            data_frame = extracted_data.get(data_cleaning_schema['data_attr'])

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
                cleaned_data[data_cleaning_schema['data_attr']] = cleaned_dataframe
            else:
                logger.error(
                    f'Dados de {data_cleaning_schema["name"].lower()} não foram extraídos corretamente.')

        return cleaned_data

    def transform_for_analysis(self, cleaned_data: Mapping[str, pd.DataFrame | None]) -> pd.DataFrame | None:
        """Transform the data for analysis."""

        logger.info('Transformando os dados para análise...')

        ruptura_data = cleaned_data.get('ruptura_data')
        estoque_data = cleaned_data.get('estoque_data')
        vendas_data = cleaned_data.get('vendas_data')

        if ruptura_data is None or estoque_data is None or vendas_data is None:
            logger.error('Dados de entrada para a transformação estão faltando. Abortando.')
            return None

        # Consolida os dados de ruptura e estoque.
        ruptura_estoque_merged = self.merger.merge_data(data_frame_left=ruptura_data,
                                                        data_frame_right=estoque_data,
                                                        left_key=['mes', 'cliente_id', 'categoria_material'],
                                                        right_key=['mes', 'cliente_id', 'categoria_material'],
                                                        how=MergeHowOptions.INNER,
                                                        suffixes=('_ruptura', '_estoque'))
        # Persistindo os dados consolidados.
        self.data_persistence.save_data(ruptura_estoque_merged,
                                        Cfg.PROCESSED_DATA.value / Cfg.RUPTURA_ESTOQUE_MERGED.value,
                                        {'sep': ';', 'encoding': 'utf-8'})

        # Consolida os dados de ruptura, estoque e vendas.
        ruptura_estoque_vendas_merged = self.merger.merge_data(data_frame_left=ruptura_estoque_merged,
                                                               data_frame_right=vendas_data,
                                                               left_key=['mes', 'cliente_id'],
                                                               right_key=['mes', 'cliente_id'],
                                                               how=MergeHowOptions.INNER,
                                                               suffixes=('_ruptura_estoque', '_vendas'))
        # Removendo colunas desnecessárias.
        ruptura_estoque_vendas_merged = ruptura_estoque_vendas_merged.drop(columns=['cod_mes',
                                                                                    'ano_ruptura_estoque',
                                                                                    'data_base_ruptura_estoque',
                                                                                    'descricao_cliente'])
        # Renomeando colunas para padronização.
        ruptura_estoque_vendas_merged = ruptura_estoque_vendas_merged.rename(columns={'data_base_vendas': 'data_base',
                                                                                      'ano_vendas': 'ano'})

        try:
            logger.info('Validando os dados após a consolidação...')
            # Validando o esquema dos dados consolidados.
            expected_order = list(CONSOLIDATED_SCHEMA.columns.keys())
            ruptura_estoque_vendas_merged = ruptura_estoque_vendas_merged.loc[:, expected_order]
            CONSOLIDATED_SCHEMA.validate(ruptura_estoque_vendas_merged, lazy=True)

            logger.success('Validação dos dados consolidados bem-sucedida.')
        except SchemaError as error:
            logger.error('Validação de dados consolidados falhou.')
            logger.error(f'Causa do erro:\n{error.failure_cases}')

            raise error

        # Persistindo os dados consolidados.
        self.data_persistence.save_data(ruptura_estoque_vendas_merged,
                                        Cfg.PROCESSED_DATA.value / Cfg.RUPTURA_ESTOQUE_VENDAS_MERGED.value,
                                        {'sep': ';', 'encoding': 'utf-8'})
        return ruptura_estoque_vendas_merged

    def load_to_destination(self, final_data: pd.DataFrame | None) -> None:
        """Load the data into the destination."""

        logger.info('Carregando os dados para o MotherDuck...')

        if final_data is not None:
            # Carregando os dados consolidados para o MotherDuck.
            self.loader.load_data(final_data, to_motherduck=True)
        else:
            logger.warning('Nenhum dado final para carregar no MotherDuck.')
