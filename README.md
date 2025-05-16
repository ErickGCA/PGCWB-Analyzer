# PGCWB Analyzer

Sistema de análise e previsão dos melhores dias para viagens entre Ponta Grossa e Curitiba, utilizando dados de trânsito em tempo real.

## [Objetivo]

Desenvolver um pipeline de engenharia de dados capaz de coletar, processar e analisar dados de trânsito entre Ponta Grossa e Curitiba (ida e volta), com o objetivo de utilizar Machine Learning para prever quais são os melhores dias da semana para viajar, baseando-se em padrões históricos de tráfego.

## [Stack Tecnológica]

- **Coleta de Dados**: Python + Requests, Google Maps API
- **Orquestração**: Apache Airflow
- **Armazenamento**: 
  - MinIO (dados brutos)
  - PostgreSQL (dados processados)
- **Processamento**: Python (ETL), SQL
- **Machine Learning**: scikit-learn, pandas
- **Visualização**: Metabase
- **Infraestrutura**: Docker, docker-compose

## [Pré-requisitos]

- Docker
- docker-compose
- Python 3.8+
- Google Maps API Key
- Git

## [Instalação]

1. Clone o repositório:
```bash
git clone https://github.com/ErickGCA/PGCWB-Analyzer.git
cd PGCWB-Analyzer
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Inicie os containers:
```bash
docker-compose up -d
```

## [Estrutura do Projeto]

```
pgcwb_analyzer/
├── airflow/          # Configurações e DAGs do Airflow
├── src/             # Código fonte
│   ├── collectors/  # Scripts de coleta
│   ├── transformers/# Transformações de dados
│   └── ml/         # Modelos de ML
├── tests/           # Testes automatizados
├── docker/          # Configurações Docker
├── docs/            # Documentação
└── notebooks/       # Jupyter notebooks
```

## [Pipeline de Dados]

1. **Coleta**: Dados são coletados a cada 2 minutos via Google Maps API
2. **Armazenamento**: 
   - Dados brutos são salvos no MinIO
   - Dados processados são armazenados no PostgreSQL
3. **Transformação**: Dados são enriquecidos com informações adicionais
4. **ML**: Modelo treinado para prever melhores dias/horários
5. **Visualização**: Dashboards no Metabase

## [Dashboards]

- Tempo real de viagem
- Análise histórica
- Previsões de melhores horários
- Comparativos de dias da semana

## [Contribuindo]

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## [Licença]

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## [Contato]


Link do Projeto: [https://github.com/ErickGCA/PGCWB-Analyzer](https://github.com/ErickGCA/PGCWB-Analyzer) 