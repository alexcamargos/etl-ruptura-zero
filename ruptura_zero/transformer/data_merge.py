#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_merge.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from typing import Literal

import pandas as pd


class DataMerger:
    """Class to merge different datasets for analysis."""

    def merge_data(self,
                   data_frame_left: pd.DataFrame,
                   data_frame_right: pd.DataFrame,
                   left_key: list[str],
                   right_key: list[str],
                   how: Literal['left', 'right', 'outer', 'inner', 'cross', 'left_anti', 'right_anti'],
                   suffixes: tuple[str, str]) -> pd.DataFrame:
        """Merge the datasets into a single DataFrame.

        Args:
            data_frame_left (pd.DataFrame): The left DataFrame to merge.
            data_frame_right (pd.DataFrame): The right DataFrame to merge.
            left_key (list[str]): The columns to join on from the left DataFrame.
            right_key (list[str]): The columns to join on from the right DataFrame.
            how (Literal['left', 'right', 'outer', 'inner', 'cross', 'left_anti', 'right_anti']): The type of merge to perform.
            suffixes (tuple[str, str]): The suffixes to apply to overlapping column names.

        Returns:
            pd.DataFrame: The merged DataFrame.
        """

        return pd.merge(data_frame_left,
                        data_frame_right,
                        left_on=left_key,
                        right_on=right_key,
                        how=how,
                        suffixes=suffixes)
