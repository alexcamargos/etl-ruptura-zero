#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_transform_service.py
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
import pandera.pandas as pa
from pandera.errors import SchemaError

from ruptura_zero.protocols.data_persistence import DataPersistenceProtocol
from ruptura_zero.protocols.transformer import DataMergerProtocol
from ruptura_zero.utilities.configurations import Config as Cfg
from ruptura_zero.utilities.merge_how_options import MergeHowOptions


class DataTransformingService:
    """Service for data transformation."""

    def __init__(self,
                 data_merger: DataMergerProtocol,
                 data_persistence: DataPersistenceProtocol,
                 data_validation_schemas: pa.DataFrameSchema) -> None:
        """Initialize the data transformation service.

        Args:
            merger (DataMergerProtocol): The data merger protocol.
            data_persistence (DataPersistenceProtocol): The data persistence protocol.
            data_validation_schemas (list[dict]): The data validation schemas.
        """

        self.data_merger = data_merger
        self.data_persistence = data_persistence
        self.data_validation_schemas = data_validation_schemas

    def _transforming(self, cleaned_data: Mapping[str, pd.DataFrame | None]) -> pd.DataFrame | None:
        """Transform the data for analysis.

        Args:
            cleaned_data (Mapping[str, pd.DataFrame | None]): The cleaned data.

        Returns:
            pd.DataFrame | None: The transformed data or None if transformation fails.
        """

        logger.info('Transformando os dados para análise...')

        ruptura_data = cleaned_data.get('ruptura_data')
        estoque_data = cleaned_data.get('estoque_data')
        vendas_data = cleaned_data.get('vendas_data')

        if ruptura_data is None or estoque_data is None or vendas_data is None:
            logger.error('Dados de entrada para a transformação estão faltando. Abortando.')
            return None

        # Consolida os dados de ruptura e estoque.
        ruptura_estoque_merged = self.data_merger.merge_data(data_frame_left=ruptura_data,
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
        ruptura_estoque_vendas_merged = self.data_merger.merge_data(data_frame_left=ruptura_estoque_merged,
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

        return ruptura_estoque_vendas_merged

    def _validate_transformed_data(self, data: pd.DataFrame | None) -> pd.DataFrame | None:
        """Validate the transformed data against the defined schemas.

        Args:
            data (pd.DataFrame | None): The transformed data to validate.

        Returns:
            pd.DataFrame | None: The validated data or None if validation fails.
        """

        try:
            logger.info('Validando os dados após a consolidação...')
            # Validando o esquema dos dados consolidados.
            expected_order = list(self.data_validation_schemas.columns.keys())
            ruptura_estoque_vendas_merged = data.loc[:, expected_order]
            self.data_validation_schemas.validate(ruptura_estoque_vendas_merged, lazy=True)

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

    def run(self, cleaned_data: Mapping[str, pd.DataFrame | None]) -> pd.DataFrame | None:
        """Run the data transformation process."""

        logger.info('Iniciando o serviço de transformação de dados...')

        # Transform the data for analysis.
        transformed_data = self._transforming(cleaned_data)

        # Validate the transformed data.
        validated_data = self._validate_transformed_data(transformed_data)

        logger.success('Processo de transformação de dados concluído com sucesso.')

        return validated_data
