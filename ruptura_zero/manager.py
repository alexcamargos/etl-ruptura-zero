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

    def extractor(self) -> None:
        """Run the extraction stage."""

        self.pipeline.extract_from_source()

    def cleaner(self) -> None:
        """Run the cleaning and validation stage."""

        self.pipeline.clean_and_validate_data()

    def transformer(self) -> None:
        """Run the transformation stage."""

        self.pipeline.transform_for_analysis()

    def loader(self) -> None:
        """Run the loading stage."""

        self.pipeline.load_to_destination()
