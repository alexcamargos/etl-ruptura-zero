#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_cleaning_service.py
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
import pandera.pandas as pa
from loguru import logger
from pandera.errors import SchemaError

from ruptura_zero.protocols.transformer import DataCleanerProtocol


class DataCleaningService:
    """Service for cleaning and validating extracted data."""

    def __init__(self, cleaner: DataCleanerProtocol, data_cleaning_schemas: list[dict]) -> None:
        """Initialize the data cleaning service.

        Args:
            cleaner (DataCleanerProtocol): The data cleaner instance.
            data_cleaning_schemas (list[dict]): The schema to be used for data cleaning.
        """

        self.cleaner = cleaner
        self.data_cleaning_schemas = data_cleaning_schemas

    def _cleaning_data(self, data: Mapping[str, pd.DataFrame | None]) -> Mapping[str, pd.DataFrame]:
        """Clean the extracted data using the defined schemas.

        Args:
            data (Mapping[str, pd.DataFrame | None]): The extracted data to clean.

        Returns:
            Mapping[str, pd.DataFrame]: The cleaned data.
        """

        cleaned_data = {}
        for schema in self.data_cleaning_schemas:
            data_frame = data.get(schema['data_attr'])
            if data_frame is not None:
                columns_mapping = schema.get('columns')
                if columns_mapping:
                    data_frame = data_frame.rename(columns=columns_mapping)
                cleaned_dataframe = self.cleaner.clean(data_frame, schema['types'])
                cleaned_data[schema['data_attr']] = cleaned_dataframe
            else:
                logger.error(f'Dados de {schema["name"].lower()} não foram extraídos corretamente.')

        return cleaned_data

    def _validate_data(self, data: Mapping[str, pd.DataFrame | None]) -> Mapping[str, pd.DataFrame]:
        """Validate the cleaned data against the defined schemas.

        Args:
            data (Mapping[str, pd.DataFrame | None]): The cleaned data to validate.

        Returns:
            Mapping[str, pd.DataFrame]: The validated data.
        """

        validated_data = {}
        for schema in self.data_cleaning_schemas:
            data_frame = data.get(schema['data_attr'])
            pandera_schema = schema.get('pandera_schema')
            if data_frame is not None and pandera_schema:
                try:
                    pandera_schema.validate(data_frame, lazy=True)
                    validated_data[schema['data_attr']] = data_frame
                except SchemaError as error:
                    logger.error(f'Validação de dados para {schema["name"]} falhou.')
                    logger.error(f'Causa do erro:\n{error.failure_cases}')
                    raise error
            else:
                logger.warning(f'Nenhum esquema Pandera encontrado para {schema["name"]}. Pulando a validação.')

        return validated_data

    def run(self, extracted_data: Mapping[str, pd.DataFrame | None]) -> Mapping[str, pd.DataFrame]:
        """Clean and validate the extracted data."""

        logger.info('Iniciando o processo de limpeza e validação dos dados extraídos...')

        cleaned_data = self._cleaning_data(extracted_data)
        validated_data = self._validate_data(cleaned_data)

        logger.success('Processo de limpeza e validação de dados concluído com sucesso.')

        return validated_data
