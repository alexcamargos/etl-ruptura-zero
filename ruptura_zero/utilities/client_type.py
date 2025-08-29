#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: client_type.py
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


class ClientType(StrEnum):
    ESPECIAL = 'ESPECIAL'
    PADRAO = 'PADRÃO'
