---
config:
  theme: neutral
  layout: dagre
---
flowchart TD
    A["Início"] --> B{"main.py"}
    B --> C{"factory.py: build_application"}
    C --> D["Instancia ExcelExtractor"] & E["Instancia DataCleaningService"] & F["Instancia DataTransformingService"] & G["Instancia DataLoader"] & H{"Instancia Pipeline"}
    H --> I{"Instancia PipelineManager"}
    I --> J{"manager.py: run_pipeline"}
    J --> K["pipeline.extract_from_source"] & M["pipeline.clean_and_validate_data"] & O["pipeline.transform_for_analysis"] & Q["pipeline.load_to_destination"]
    K --> L["Extrai dados do Excel: ruptura, estoque, vendas"]
    M --> N["Limpa e valida os dados extraídos"]
    O --> P["Transforma os dados limpos"]
    Q --> R["Carrega os dados transformados no MotherDuck"]
    R --> S["Fim"]
