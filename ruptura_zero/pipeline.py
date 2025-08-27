#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: pipeline.py
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

from ruptura_zero.extractor.excel_extractor import ExcelExtractor


class Pipeline:
    """Defines the ETL pipeline for the Ruptura Zero project."""

    def __init__(self, extractor: ExcelExtractor) -> None:
        """Initialize the Pipeline."""

        logger.info("Initializing Pipeline...")

        # Set the extractor
        self.extractor = extractor

        # Initialize data attributes
        self.ruptura_data = None
        self.vendas_data = None
        self.estoque_data = None

    def extract_from_source(self) -> None:
        """Extract data from the source."""

        logger.info("Extracting data from source...")

        sheets = self.extractor.extract()

        self.ruptura_data = sheets.get('01_BD_Ruptura')
        self.vendas_data = sheets.get('02_BD_Estoque')
        self.estoque_data = sheets.get('03_BD_Vendas')

        if (self.ruptura_data is None or
                self.vendas_data is None or
                self.estoque_data is None):
            logger.error('Data extraction failed.')

    def clean_and_validate_data(self) -> None:
        """Clean and validate the data."""

        logger.info("Cleaning and validating data...")

    def transform_for_analysis(self) -> None:
        """Transform the data for analysis."""

        logger.info("Transforming data for analysis...")

    def load_to_destination(self) -> None:
        """Load the data into the destination."""

        logger.info("Loading data to destination...")
