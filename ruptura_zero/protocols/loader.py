#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: loader.py
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


class LoaderProtocol(Protocol):
    """Protocol for data loaders."""

    def load_data(self, data: pd.DataFrame, to_motherduck: bool) -> None:
        raise NotImplementedError('You should implement this method.')
