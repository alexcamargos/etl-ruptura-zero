#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: merge_how_options.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from enum import StrEnum


class MergeHowOptions(StrEnum):
    LEFT = 'left'
    RIGHT = 'right'
    OUTER = 'outer'
    INNER = 'inner'
    CROSS = 'cross'
    LEFT_ANTI = 'left_anti'
    RIGHT_ANTI = 'right_anti'
