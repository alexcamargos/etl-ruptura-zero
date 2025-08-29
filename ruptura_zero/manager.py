#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: manager.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from loguru import logger

from ruptura_zero.pipeline import Pipeline


class PipelineManager:
    """Orchestrates the ETL pipeline stages."""

    def __init__(self, pipeline: Pipeline) -> None:
        """Initialize the PipelineManager.

        Args:
            pipeline (Pipeline): The ETL pipeline instance.
        """

        logger.info('Inicializando o Pipeline Manager...')

        self.pipeline = pipeline

    def run_pipeline(self) -> None:
        """Run the entire ETL pipeline."""

        # Extraindo os dados brutos.
        raw_data = self.pipeline.extract_from_source()

        # Limpando e validando os dados.
        cleaned_data = self.pipeline.clean_and_validate_data(raw_data)

        # Transformando os dados para análise.
        transformed_data = self.pipeline.transform_for_analysis(cleaned_data)

        # Carregando os dados transformados.
        self.pipeline.load_to_destination(transformed_data)
