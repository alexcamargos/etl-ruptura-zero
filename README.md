# Projeto "Ruptura Zero": Análise de Vendas e Estoque

> _Um pipeline de ETL robusto para transformar dados de vendas em insights acionáveis, diagnosticando rupturas de estoque e otimizando o inventário._

[![LinkedIn](https://img.shields.io/badge/%40alexcamargos-230A66C2?style=social&logo=LinkedIn&label=LinkedIn&color=white)](https://www.linkedin.com/in/alexcamargos)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)


## 💡 Sobre o Projeto
O "Ruptura Zero" é um pipeline de ETL desenvolvido em Python para diagnosticar a causa raiz da queda de vendas em uma empresa. O projeto nasceu da hipótese de que a má gestão de inventário estava gerando ruptura de estoque (falta de produtos), impactando diretamente a receita.

Este pipeline automatiza a extração de dados brutos de vendas e estoque de arquivos Excel, aplica um rigoroso processo de limpeza e transformação, e utiliza `Pandera` para garantir a integridade dos dados. O resultado final é um dataset consolidado e confiável, pronto para análise, permitindo que a área de negócio identifique exatamente quais produtos estão em falta e onde, transformando dados em um plano de ação para otimização de inventário e recuperação do crescimento.


- [Projeto "Ruptura Zero": Análise de Vendas e Estoque](#projeto-ruptura-zero-análise-de-vendas-e-estoque)
  - [💡 Sobre o Projeto](#-sobre-o-projeto)
  - [🛠️ Stack de Tecnologias](#️-stack-de-tecnologias)
  - [✨ Funcionalidades Principais](#-funcionalidades-principais)
  - [🏛️ Arquitetura e Padrões](#️-arquitetura-e-padrões)
  - [🚀 Como Instalar e Executar](#-como-instalar-e-executar)
  - [📊 Resultados e Entregáveis](#-resultados-e-entregáveis)
  - [✍️ Autor](#️-autor)
  - [📜 Licença](#-licença)


## 🛠️ Stack de Tecnologias
| Categoria | Ferramenta |
| :--- | :--- |
| **Gerenciador de Dependências** | ![UV](https://img.shields.io/badge/uv-0.1.11-purple?style=flat-square) |
| **Linguagem Principal** | ![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python) |
| **Análise de Dados** | ![Pandas](https://img.shields.io/badge/Pandas-2.3.2-blue?style=flat-square&logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-2.0.2-blue?style=flat-square&logo=numpy) |
| **Validação de Dados** | ![Pandera](https://img.shields.io/badge/Pandera-0.14.5-blue?style=flat-square) |
| **Data Warehouse** | ![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black) ![MotherDuck](https://img.shields.io/badge/MotherDuck-000000?style=flat-square&logo=motherduck) |


## ✨ Funcionalidades Principais
- **🔌 Extração de Dados**: Leitura e parsing de múltiplas fontes de dados em formato `.xlsx`.
- **🧹 Limpeza e Transformação**: Normalização de formatos, tratamento de valores nulos e enriquecimento de dados.
- **🛡️ Validação Robusta**: Implementação de esquemas `Pandera` para garantir a qualidade e a consistência dos dados em cada etapa.
- **📊 Análise e Agregação**: Cruzamento de tabelas de vendas e estoque para o cálculo preciso de métricas de ruptura.
- **📤 Carga de Dados**: Exportação dos dados processados para arquivos `.csv` e carga em um data warehouse serverless **MotherDuck** para análise SQL imediata.


## 🏛️ Arquitetura e Padrões
O projeto foi estruturado seguindo o padrão **ETL (Extract, Transform, Load)** para garantir um fluxo de dados claro e manutenível.

- **/ruptura_zero/extractor**: Módulos responsáveis pela extração de dados de fontes externas (ex: planilhas Excel).
- **/ruptura_zero/transformer**: Contém a lógica de negócio para limpeza, transformação e validação dos dados. Utiliza **Pandera** para definir e aplicar esquemas de validação, garantindo a robustez do pipeline.
- **/ruptura_zero/services**: Orquestra as etapas limpesa e transformação do pipeline, desacoplando do pipeline principal o status de cada etapa.
- **/ruptura_zero/loader**: Responsável por carregar os dados transformados em um destino final, arquivos CSV consolidados e data warehouse na nuvem (MotherDuck).
- **/ruptura_zero/factory.py**: Aplica o padrão de projeto **Factory** para criar instâncias de componentes do pipeline de forma desacoplada.

Essa arquitetura modular e o uso de validação de dados demonstram um foco em criar um sistema de dados confiável e escalável.


## 🚀 Como Instalar e Executar

**Pré-requisitos:**
- Python 3.11 ou superior
- `uv` instalado (`pip install uv`)

**Passos:**

1.  Clone o repositório:
    ```bash
    git clone https://github.com/alexcamargos/etl_ruptura_zero.git
    cd etl_ruptura_zero
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    uv venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```

3.  Instale as dependências do projeto:
    ```bash
    uv pip sync pyproject.toml
    ```

4.  Execute o pipeline de ETL:
    ```bash
    python main.py
    # Ao final da execução, verifique a pasta `data/processed/` pelos arquivos gerados.
    ```

## 📊 Resultados e Entregáveis
Ao final da execução, o pipeline produz dois tipos de entregáveis, prontos para diferentes casos de uso:

**1. Arquivos CSV Consolidados**
Para análise local, portabilidade ou importação rápida em outras ferramentas, os seguintes arquivos são gerados na pasta `data/processed/`:
- `ruptura_estoque_vendas.csv`: O dataset final consolidado, contendo a união dos dados de vendas e estoque.

**2. Data Warehouse na Nuvem (MotherDuck)**
Para análise interativa e escalável, o dataset consolidado é carregado em uma tabela no MotherDuck. Isso o torna imediatamente acessível para:
- Consultas complexas usando SQL.
- Conexão direta com ferramentas de Business Intelligence (BI) como Tableau ou Power BI.


## ✍️ Autor

Feito com ❤️ por [Alexsander Lopes Camargos](https://github.com/alexcamargos) 👋 Entre em contato!

[![GitHub](https://img.shields.io/badge/-AlexCamargos-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=github&logoColor=white&link=https://github.com/alexcamargos)](https://github.com/alexcamargos)
[![Twitter Badge](https://img.shields.io/badge/-@alcamargos-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=twitter&logoColor=white&link=https://twitter.com/alcamargos)](https://twitter.com/alcamargos)
[![Linkedin Badge](https://img.shields.io/badge/-alexcamargos-1ca0f1?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/alexcamargos/)](https://www.linkedin.com/in/alexcamargos/)
[![Gmail Badge](https://img.shields.io/badge/-alcamargos@vivaldi.net-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=Gmail&logoColor=white&link=mailto:alcamargos@vivaldi.net)](mailto:alcamargos@vivaldi.net)


## 📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
