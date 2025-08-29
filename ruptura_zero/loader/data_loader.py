#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_loader.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

import os

import duckdb as db
import pandas as pd
from dotenv import load_dotenv
from loguru import logger


class DataLoader:
    def __init__(self, table_name: str = 'ruptura_zero_analysis') -> None:
        """Initialize the DataLoader.

        Args:
            table_name (str): The name of the table to load data into.
        """

        self.table_name = table_name

        # Carregando o token do MotherDuck.
        self._load_token()

    def _load_token(self) -> None:
        """Load the MotherDuck token from environment variables."""

        # Carregando as variáveis de ambiente do arquivo .env.
        load_dotenv()
        motherduck_token = os.getenv('MOTHERDUCK_TOKEN')

        if not motherduck_token:
            logger.error('O token do MotherDuck (MOTHERDUCK_TOKEN) não foi encontrado no ambiente.')
            logger.error('Por favor, crie um arquivo .env ou defina a variável de ambiente.')
            logger.error('Você pode obter um token em: https://app.motherduck.com/')

            raise ValueError('MOTHERDUCK_TOKEN não está configurado.')

        self.token = motherduck_token

    def load_data_to_motherduck(self, data: pd.DataFrame) -> None:
        """Load data into MotherDuck.

        Args:
            data (pd.DataFrame): The data to load into MotherDuck.
        """

        try:
            logger.info('Estabelecendo conexão com o MotherDuck...')

            with db.connect(database='md:', read_only=False) as connection:
                logger.success('Conexão com MotherDuck estabelecida com sucesso.')
                logger.info(f'Preparando para carregar dados na tabela "{self.table_name}"...')

                connection.register('data_to_load', data)
                connection.execute(f'CREATE OR REPLACE TABLE {self.table_name} AS SELECT * FROM data_to_load')

                # Checando o número de linhas carregadas para o MotherDuck.
                count_result = connection.execute(f'SELECT COUNT(*) FROM {self.table_name}').fetchone()
                if count_result:
                    logger.success(f'Dados carregados com sucesso na tabela "{self.table_name}" no MotherDuck.')
                    logger.info(f'{count_result[0]} linhas foram carregadas na tabela "{self.table_name}"')
                else:
                    logger.warning('Não foi possível verificar o número de linhas carregadas.')

        except db.Error as error:
            logger.error(f'Ocorreu um erro ao carregar os dados para o MotherDuck: {error}')
            raise
