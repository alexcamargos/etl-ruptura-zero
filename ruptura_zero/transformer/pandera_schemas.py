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

CONSOLIDATED_SCHEMA = pa.DataFrameSchema(
    columns={
        'data_base': pa.Column(pa.Int64,
                               nullable=False,
                               description='Data base da observação (YYYYMM)'),
        'ano': pa.Column(pa.Int64,
                         nullable=False,
                         checks=pa.Check.in_range(2020, 2025),
                         description='Ano da observação (YYYY).'),
        'mes': pa.Column(pa.Int64,
                         nullable=False,
                         checks=pa.Check.in_range(1, 12),
                         description='Mês da observação em formato numérico (1-12)'),
        'cliente_id': pa.Column(pa.String,
                                nullable=False,
                                checks=pa.Check.str_length(2, 2),
                                description='Código identificador único do cliente'),
        'nome_cliente': pa.Column(pa.String,
                                  nullable=False,
                                  description='Nome do cliente (ex: ESMERALDA, RUBI)'),
        'tipo_cliente': pa.Column(pa.String,
                                  checks=pa.Check.isin(['ESPECIAL', 'PADRÃO']),
                                  nullable=False,
                                  description='Classificação do cliente'),
        'cidade': pa.Column(pa.String,
                            nullable=False,
                            description='Cidade do cliente'),
        'uf': pa.Column(pa.String,
                        nullable=False,
                        checks=[pa.Check.str_length(2, 2),
                                pa.Check.isin(['AC', 'AL', 'AM', 'AP', 'BA',
                                               'CE', 'DF', 'ES', 'GO', 'MA',
                                               'MG', 'MS', 'MT', 'PA', 'PB',
                                               'PE', 'PI', 'PR', 'RJ', 'RN',
                                               'RO', 'RR', 'RS', 'SC', 'SE',
                                               'SP', 'TO'])],
                        description='Unidade Federativa (UF) do cliente'),
        'pais': pa.Column(pa.String,
                          nullable=False,
                          checks=pa.Check.isin(['BR']),
                          description='País do cliente'),
        'contato_cliente': pa.Column(pa.String,
                                     nullable=False,
                                     description='Nome do contato no cliente'),
        'categoria_material': pa.Column(pa.String,
                                        nullable=False,
                                        description='Categoria do produto'),
        'valor_ruptura': pa.Column(pa.Float64,
                                   nullable=False,
                                   checks=pa.Check.ge(0),
                                   description='Valor em R$ da venda perdida por falta de produto'),
        'valor_pedido': pa.Column(pa.Float64,
                                  nullable=False,
                                  checks=pa.Check.ge(0),
                                  description='Valor total do pedido para a categoria'),
        'volume_ruptura_und': pa.Column(pa.Int64,
                                        nullable=False,
                                        checks=pa.Check.ge(0),
                                        description='Volume em unidades da venda perdida'),
        'percent_ruptura': pa.Column(pa.Float64,
                                     nullable=False,
                                     checks=[pa.Check.ge(0), pa.Check.le(100)],
                                     description='Percentual de ruptura (valor_ruptura / valor_pedido)'),
        'estoque': pa.Column(pa.Int64,
                             nullable=False,
                             checks=pa.Check.ge(0),
                             description='Quantidade de produto em estoque (unidades)'),
        'ddv': pa.Column(pa.Float64,
                         nullable=False,
                         checks=pa.Check.ge(0),
                         description='Demanda Diária de Venda (unidades/dia)'),
        'cobertura_dias': pa.Column(pa.Int64,
                                    nullable=False,
                                    checks=pa.Check.ge(0),
                                    description='Número de dias que o estoque atual cobre a demanda'),
        'valor_volume_real': pa.Column(pa.Int64,
                                       nullable=False,
                                       checks=pa.Check.ge(0),
                                       description='Volume total de vendas do cliente no mês')
    },
    strict=True,
    ordered=True
)
