#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: pandera_schemas.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

import pandera.pandas as pa

# Esquema de validação para os dados de ruptura.
RUPTURA_SCHEMA = pa.DataFrameSchema(
    columns={
        'data_base': pa.Column(int, nullable=False, coerce=True),
        'cliente_id': pa.Column(str, nullable=False, coerce=True),
        'descricao_cliente': pa.Column(str, nullable=False, coerce=True),
        'categoria_material': pa.Column(str, nullable=False, coerce=True),
        'valor_ruptura': pa.Column(float, nullable=False, coerce=True),
        'valor_pedido': pa.Column(float, nullable=False, coerce=True),
        'volume_ruptura_und': pa.Column(int, nullable=False, coerce=True),
        'percent_ruptura': pa.Column(float, nullable=False, coerce=True),
        'ano': pa.Column(int, nullable=False, coerce=True),
        'mes': pa.Column(int, nullable=False, coerce=True),
    },
    strict=True,
    ordered=True
)

# Esquema de validação para os dados de estoque.
ESTOQUE_SCHEMA = pa.DataFrameSchema(
    columns={
        'cod_mes': pa.Column(str, nullable=False, coerce=True),
        'cliente_id': pa.Column(str, nullable=False, coerce=True),
        'nome_cliente': pa.Column(str, nullable=False, coerce=True),
        'categoria_material': pa.Column(str, nullable=False, coerce=True),
        'estoque': pa.Column(int, nullable=False, coerce=True),
        'ddv': pa.Column(float, nullable=False, coerce=True),
        'cobertura_dias': pa.Column(int, nullable=False, coerce=True),
        'tipo_cliente': pa.Column(str, nullable=False, coerce=True),
        'contato_cliente': pa.Column(str, nullable=False, coerce=True),
        'mes': pa.Column(int, nullable=False, coerce=True),
    },
    strict=True,
    ordered=True
)

# Esquema de validação para os dados de vendas.
VENDAS_SCHEMA = pa.DataFrameSchema(
    columns={
        'data_base': pa.Column(int, nullable=False, coerce=True),
        'cliente_id': pa.Column(str, nullable=False, coerce=True),
        'valor_volume_real': pa.Column(float, nullable=False, coerce=True),
        'cidade': pa.Column(str, nullable=False, coerce=True),
        'uf': pa.Column(str, nullable=False, coerce=True),
        'pais': pa.Column(str, nullable=False, coerce=True),
        'ano': pa.Column(int, nullable=False, coerce=True),
        'mes': pa.Column(int, nullable=False, coerce=True),
    },
    strict=True,
    ordered=True
)
