#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_persistence.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from pathlib import Path

import pandas as pd
from loguru import logger


class DataPersistence:
    """Class to handle data persistence operations."""

    def save_data(self, data: pd.DataFrame, storage_path: Path, options: dict) -> None:
        """Save the DataFrame to a file.

        Args:
            data (pd.DataFrame): The DataFrame to save.
            options (dict): Additional options to pass to the to_csv method.
        """

        logger.info(f'Salvando dados em {storage_path}...')

        data.to_csv(storage_path, index=False, **options)
