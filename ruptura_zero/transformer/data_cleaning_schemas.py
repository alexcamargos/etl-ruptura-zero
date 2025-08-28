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
        'columns': {
            'DT_MES': 'data_base',
            'COD_CLIENTE': 'cliente_id',
            'CLIENTE_DESCRICAO': 'descricao_cliente',
            'MATERIAL_DESCRICAO_CATEGORIA': 'categoria_material',
            'Valor Ruptura_$': 'valor_ruptura',
            'Valor Pedido_$': 'valor_pedido',
            'Volume ruptura_und': 'volume_ruptura_und',
            'Ruptura_%': 'percent_ruptura'
        },
        'types': {
            'data_base': 'data-base',
            'cliente_id': 'string',
            'descricao_cliente': 'string',
            'categoria_material': 'string',
            'valor_ruptura': 'monetary',
            'valor_pedido': 'monetary',
            'volume_ruptura_und': 'integer',
            'percent_ruptura': 'percent',
            'ano': 'integer',
            'mes': 'integer'
        },
        'pandera_schema': RUPTURA_SCHEMA
    },
    {
        'name': '02_BD_Estoque',
        'data_attr': 'estoque_data',
        'columns': {
            'MES': 'mes',
            'COD_CLIENTE': 'cliente_id',
            'NOME CLIENTE': 'nome_cliente',
            'DESCRICAO_CATEGORIA': 'categoria_material',
            'ESTOQUE': 'estoque',
            'DDV': 'ddv',
            'COBERTURA_DIAS': 'cobertura_dias',
            'TIPO_CLIENTE': 'tipo_cliente',
            'CONTATO CLIENTE': 'contato_cliente'
        },
        'types': {
            'mes': 'string',
            'cliente_id': 'string',
            'nome_cliente': 'string',
            'categoria_material': 'string',
            'estoque': 'integer',
            'ddv': 'float',
            'cobertura_dias': 'integer',
            'tipo_cliente': 'string',
            'contato_cliente': 'string'
        },
        'pandera_schema': ESTOQUE_SCHEMA
    },
    {
        'name': '03_BD_Vendas',
        'data_attr': 'vendas_data',
        'columns': {
            'DT_MES': 'data_base',
            'COD CLIEN': 'cliente_id',
            'VLR_VOLUME_REAL': 'valor_volume_real',
            'CIDADE': 'cidade',
            'UF': 'uf',
            'PAIS': 'pais'
        },
        'types': {
            'data_base': 'data-base',
            'cliente_id': 'string',
            'valor_volume_real': 'string',
            'cidade': 'string',
            'uf': 'string',
            'pais': 'string',
            'ano': 'integer',
            'mes': 'integer'
        },
        'pandera_schema': VENDAS_SCHEMA
    },
]
