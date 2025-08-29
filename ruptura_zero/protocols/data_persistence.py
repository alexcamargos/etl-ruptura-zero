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
from typing import Protocol

import pandas as pd


class DataPersistenceProtocol(Protocol):
    """Protocol for data persistence mechanisms."""

    def save_data(self, data: pd.DataFrame, storage_path: Path, options: dict) -> None:
        raise NotImplementedError('You should implement this method.')
