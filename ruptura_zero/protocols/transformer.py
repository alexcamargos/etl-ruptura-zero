#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: transformer.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from typing import Protocol

import pandas as pd

from ruptura_zero.utilities.merge_how_options import MergeHowOptions


class DataCleanerProtocol(Protocol):
    """Protocol for data cleaners."""

    def clean(self, data: pd.DataFrame, column_types: dict) -> pd.DataFrame:
        raise NotImplementedError('You should implement this method.')


class DataMergerProtocol(Protocol):
    """Protocol for data mergers."""

    def merge_data(self,
                   data_frame_left: pd.DataFrame,
                   data_frame_right: pd.DataFrame,
                   left_key: list[str],
                   right_key: list[str],
                   how: MergeHowOptions,
                   suffixes: tuple[str, str]) -> pd.DataFrame:
        raise NotImplementedError('You should implement this method.')
