#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: excel_extractor.py
#  Version: 0.0.1
#
#  Summary: Ruptura Zero: Análise de Vendas e Estoque
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from pathlib import Path

import pandas as pd
from loguru import logger


class ExcelExtractor:
    """Extracts data from Excel files."""

    def __init__(self, file_path: Path) -> None:
        """Initialize the ExcelExtractor.

        Args:
            file_path (str): The path to the Excel file.
        """

        self.file_path = file_path

    def extract_all_sheets(self) -> dict[str, pd.DataFrame]:
        """Extract all sheets from the Excel file.

        Returns:
            dict[str, pd.DataFrame]: A dictionary with sheet names as keys and DataFrames as values.
        """

        logger.info(f"Extracting all sheets from Excel file: {self.file_path}")

        try:
            xls = pd.ExcelFile(self.file_path)
            sheets = {str(sheet_name): xls.parse(sheet_name) for sheet_name in xls.sheet_names}

            logger.info("All sheets extraction successful.")

            return sheets
        except Exception as error:
            logger.error(f"Error extracting all sheets from Excel file: {error}")

            return {}

    def extract(self) -> dict[str, pd.DataFrame]:
        """Extract data from the Excel file."""

        return self.extract_all_sheets()
