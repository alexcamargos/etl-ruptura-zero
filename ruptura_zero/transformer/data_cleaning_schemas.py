#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_cleaning_schemas.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from ruptura_zero.transformer.pandera_schemas import ESTOQUE_SCHEMA, RUPTURA_SCHEMA, VENDAS_SCHEMA

DATA_CLEANING_SCHEMAS = [
    {
        'name': '01_BD_Ruptura',
        'data_attr': 'ruptura_data',
        'types': {
            'dt_mes': 'date',
            'cod_cliente': 'string',
            'cliente_descricao': 'string',
            'material_descricao_categoria': 'string',
            'valor_ruptura_$': 'monetary',
            'valor_pedido_$': 'monetary',
            'volume_ruptura_und': 'integer',
            'ruptura_%': 'percent',
            'ano': 'integer',
            'mes': 'integer'
        },
        'pandera_schema': RUPTURA_SCHEMA
    },
    {
        'name': '02_BD_Estoque',
        'data_attr': 'estoque_data',
        'types': {
            'mes': 'string',
            'cod_cliente': 'string',
            'nome_cliente': 'string',
            'descricao_categoria': 'string',
            'estoque': 'integer',
            'ddv': 'float',
            'cobertura_dias': 'integer',
            'tipo_cliente': 'string',
            'contato_cliente': 'string'
        },
        'pandera_schema': VENDAS_SCHEMA
    },
    {
        'name': '03_BD_Vendas',
        'data_attr': 'vendas_data',
        'types': {
            'dt_mes': 'date',
            'cod_clien': 'string',
            'vlr_volume_real': 'integer',
            'cidade': 'string',
            'uf': 'string',
            'pais': 'float',
            'ano': 'integer',
            'mes': 'integer'
        },
        'pandera_schema': ESTOQUE_SCHEMA
    }
]
