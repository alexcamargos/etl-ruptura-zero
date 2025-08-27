#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: cleaner.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

import pandas as pd


class DataCleaner:
    """Cleans and preprocesses data for analysis."""

    def _normalize_columns_names(self, data: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names by stripping whitespace and converting to lowercase.

        Args:
            data (pd.DataFrame): The data to normalize column names for.

        Returns:
            pd.DataFrame: The data with normalized column names.
        """

        data.columns = data.columns.str.strip() \
                                   .str.replace(' ', '_') \
                                   .str.lower()

        return data

    def _normalize_numeric_columns(self, data: pd.DataFrame, numeric_columns: list) -> pd.DataFrame:
        """Normalize numeric columns by converting them to a consistent format.

        Args:
            data (pd.DataFrame): The data to normalize numeric columns for.
            numeric_columns (list): The names of the numeric columns to normalize.

        Returns:
            pd.DataFrame: The data with normalized numeric columns.
        """

        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return data

    def _normalize_monetary_columns(self, data: pd.DataFrame, monetary_columns: list) -> pd.DataFrame:
        """Normalize monetary columns by removing currency symbols and converting to numeric.

        Args:
            data (pd.DataFrame): The data to normalize monetary columns for.
            monetary_columns (list): The names of the columns to normalize.

        Returns:
            pd.DataFrame: The data with normalized monetary columns.
        """

        for column in monetary_columns:
            data[column] = data[column].str.replace('R$', '', regex=False) \
                                       .str.replace('.', '', regex=False) \
                                       .str.replace(',', '.', regex=False)

        return data

    def _extract_year_and_month(self, data: pd.DataFrame, date_columns: list) -> pd.DataFrame:
        """Extract year and month from date columns."""

        for column in date_columns:
            data['ano'] = data[column].astype(str).str[:4]
            data['mes'] = data[column].astype(str).str[-2:]

        return data

    def _normalize_percent_columns(self, data: pd.DataFrame, percent_columns: list) -> pd.DataFrame:

        for column in percent_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')

        return data

    def _remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows from the data.

        Args:
            data (pd.DataFrame): The data to remove duplicates from.

        Returns:
            pd.DataFrame: The cleaned data without duplicates.
        """

        return data.drop_duplicates()

    def _fill_missing_values(self, data: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
        """Fill missing values in the data.

        Args:
            data (pd.DataFrame): The data to fill missing values in.
            strategy (str, optional): The strategy to use for filling missing values.
                Options are "mean", "median", or "mode". Defaults to "mean".

        Returns:
            pd.DataFrame: The cleaned data with missing values filled.
        """

        match strategy:
            case "mean":
                data = data.fillna(data.mean(numeric_only=True))
            case "median":
                data = data.fillna(
                    data.median(numeric_only=True))
            case "mode":
                data = data.fillna(data.mode().iloc[0])
            case _:
                raise ValueError(f"Estratégia de preenchimento desconhecida: '{strategy}'")

        return data

    def clean(self, data: pd.DataFrame, column_types: dict) -> pd.DataFrame:
        """Perform all cleaning steps.

        Args:
            data (pd.DataFrame): The data to clean.
            column_types (dict): The expected column types.

        Returns:
            pd.DataFrame: The cleaned data.
        """
        # Normaliza os nomes das colunas.
        data = self._normalize_columns_names(data)

        # Normaliza as colunas numéricas.
        numeric_columns = [column for column, dtype in column_types.items() if dtype == 'integer']
        data = self._normalize_numeric_columns(data, numeric_columns)

        # Normaliza as colunas monetárias.
        monetary_columns = [column for column, dtype in column_types.items() if dtype == 'monetary']
        data = self._normalize_monetary_columns(data, monetary_columns)

        # Normaliza as colunas percentuais.
        percent_columns = [column for column, dtype in column_types.items() if dtype == 'percent']
        data = self._normalize_percent_columns(data, percent_columns)

        # Extrai o ano e o mês das colunas de data.
        date_columns = [column for column, dtype in column_types.items() if dtype == 'date']
        data = self._extract_year_and_month(data, date_columns)

        # Remove valores duplicados.
        data = self._remove_duplicates(data)

        # Preenche valores ausentes.
        data = self._fill_missing_values(data)

        return data
