#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: main.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

from loguru import logger

from ruptura_zero.factory import build_application


def main() -> None:
    """Run the main ETL pipeline."""

    logger.info('Ruptura Zero: Análise de Vendas e Estoques.')

    # Run the ETL pipeline.
    pipeline_manager = build_application()
    pipeline_manager.run_pipeline()


if __name__ == "__main__":
    # Starting the ETL process.
    main()
