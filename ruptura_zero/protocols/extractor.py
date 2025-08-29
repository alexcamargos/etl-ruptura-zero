#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: extractor.py
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


class ExtractorProtocol(Protocol):
    """Protocol for data extractors."""

    def extract(self) -> dict[str, pd.DataFrame]:
        raise NotImplementedError('You should implement this method.')
