#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: configurations.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from enum import Enum
from pathlib import Path


class Config(Enum):
    """Configuration settings for project Ruptura Zero."""

    BASE_DIRECTORY = Path.cwd()
    LOG_DIRECTORY = BASE_DIRECTORY / 'logs'
    RAW_DATA = BASE_DIRECTORY / 'data' / 'raw'
    CLEANED_DATA = BASE_DIRECTORY / 'data' / 'cleaned'
    PROCESSED_DATA = BASE_DIRECTORY / 'data' / 'processed'
