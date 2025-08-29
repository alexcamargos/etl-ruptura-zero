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

import pandas as pd
from loguru import logger

from ruptura_zero.utilities.merge_how_options import MergeHowOptions


class DataMerger:
    """Class to merge different datasets for analysis."""

    def merge_data(self,
                   data_frame_left: pd.DataFrame,
                   data_frame_right: pd.DataFrame,
                   left_key: list[str],
                   right_key: list[str],
                   how: MergeHowOptions,
                   suffixes: tuple[str, str]) -> pd.DataFrame:
        """Merge the datasets into a single DataFrame.

        Args:
            data_frame_left (pd.DataFrame): The left DataFrame to merge.
            data_frame_right (pd.DataFrame): The right DataFrame to merge.
            left_key (list[str]): The columns to join on from the left DataFrame.
            right_key (list[str]): The columns to join on from the right DataFrame.
            how (MergeHowOptions): The type of merge to perform.
            suffixes (tuple[str, str]): The suffixes to apply to overlapping column names.

        Returns:
            pd.DataFrame: The merged DataFrame.
        """

        logger.info(
            f'Consolidando os dados: {data_frame_left.shape[0]} linhas do lado esquerdo, '
            f'{data_frame_right.shape[0]} linhas do lado direito')
        logger.info(f'Usando chaves de junção: {left_key} (esquerda) e {right_key} (direita)')
        logger.info(f'Tipo de merge: {how.value}')
        logger.info(f'Sufixos aplicados: {suffixes}')

        return pd.merge(data_frame_left,
                        data_frame_right,
                        left_on=left_key,
                        right_on=right_key,
                        how=how.value,
                        suffixes=suffixes)
