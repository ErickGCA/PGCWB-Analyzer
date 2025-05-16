# PGCWB Analyzer - Roadmap

## Visão Geral
Projeto para análise e previsão dos melhores dias para viagens entre Ponta Grossa e Curitiba, utilizando dados de trânsito em tempo real.

## Stack Tecnológica

### Coleta de Dados
- Python + Requests
- Google Maps API
- Airflow (orquestração)

### Armazenamento
- MinIO (dados brutos)
- PostgreSQL (dados processados)

### Processamento
- Python (ETL)
- SQL (transformações)

### Machine Learning
- scikit-learn
- pandas

### Visualização
- Metabase

### Infraestrutura
- Docker
- docker-compose

## Fases do Projeto

### Fase 1 — Coleta e Armazenamento
- [ ] Configurar ambiente de desenvolvimento
  - [ ] Criar estrutura de diretórios
  - [ ] Configurar Docker e docker-compose
  - [ ] Configurar MinIO
  - [ ] Configurar PostgreSQL
  - [ ] Configurar Airflow

- [ ] Implementar coleta de dados
  - [ ] Desenvolver script de coleta do Google Maps
  - [ ] Implementar lógica de ida/volta
  - [ ] Configurar intervalo de coleta (2 minutos)
  - [ ] Implementar logs de coleta

- [ ] Configurar armazenamento
  - [ ] Definir estrutura de buckets no MinIO
  - [ ] Criar schemas no PostgreSQL
  - [ ] Implementar backup automático

### Fase 2 — Transformação
- [ ] Desenvolver pipeline de transformação
  - [ ] Criar DAGs no Airflow
  - [ ] Implementar transformações básicas
  - [ ] Adicionar dimensões (dia da semana, horário)
  - [ ] Criar validações de dados

- [ ] Implementar enriquecimento
  - [ ] Adicionar informações de feriados
  - [ ] Criar faixas de horário
  - [ ] Implementar cálculos de médias

### Fase 3 — Modelagem
- [ ] Preparar dados para ML
  - [ ] Criar features relevantes
  - [ ] Implementar normalização
  - [ ] Separar dados de treino/teste

- [ ] Desenvolver modelo
  - [ ] Treinar modelo com scikit-learn
  - [ ] Implementar validação cruzada
  - [ ] Ajustar hiperparâmetros
  - [ ] Avaliar performance

- [ ] Implementar pipeline de predição
  - [ ] Criar DAG de predição
  - [ ] Implementar armazenamento de previsões
  - [ ] Configurar atualização do modelo

### Fase 4 — Visualização
- [ ] Configurar Metabase
  - [ ] Conectar com PostgreSQL
  - [ ] Configurar usuários e permissões

- [ ] Criar dashboards
  - [ ] Dashboard de tempo real
  - [ ] Dashboard de previsões
  - [ ] Dashboard de análise histórica

- [ ] Implementar visualizações
  - [ ] Gráficos de tempo de viagem
  - [ ] Mapas de calor por dia/hora
  - [ ] Comparativos de previsões

### Fase 5 — Automação e Documentação
- [ ] Finalizar containerização
  - [ ] Otimizar Dockerfiles
  - [ ] Configurar volumes
  - [ ] Implementar healthchecks

- [ ] Documentar projeto
  - [ ] Criar README detalhado
  - [ ] Documentar APIs
  - [ ] Criar guias de uso
  - [ ] Documentar arquitetura

- [ ] Implementar monitoramento
  - [ ] Configurar alertas
  - [ ] Implementar métricas
  - [ ] Criar dashboard de status

## Estrutura de Diretórios
```
pgcwb_analyzer/
├── airflow/
│   ├── dags/
│   └── plugins/
├── src/
│   ├── collectors/
│   ├── transformers/
│   └── ml/
├── tests/
├── docker/
├── docs/
└── notebooks/
```

## Próximos Passos
1. Configurar ambiente de desenvolvimento
2. Implementar coleta inicial de dados
3. Configurar armazenamento
4. Desenvolver primeira versão do pipeline 