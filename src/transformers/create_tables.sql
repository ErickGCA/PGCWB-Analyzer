-- Tabela para dados transformados
-- Tabela para dados transformados
CREATE TABLE IF NOT EXISTS traffic_data_transformed (
    id SERIAL PRIMARY KEY,
    -- Coluna para rastrear o ID do dado original na tabela traffic_data
    raw_data_id INTEGER, -- SUGESTÃO: Adicionar esta coluna
    timestamp TIMESTAMP WITH TIME ZONE, -- UTC (original da coleta)
    -- timestamp_local TIMESTAMP WITH TIME ZONE, -- OPCIONAL: Se quiser armazenar o timestamp já convertido para 'America/Sao_Paulo'
    data DATE,
    hora INTEGER,
    minuto INTEGER,
    dia_semana VARCHAR(20), -- Aumentado um pouco para nomes mais longos de dias da semana em alguns locales
    dia_semana_num INTEGER,
    faixa_horario VARCHAR(15), -- Aumentado um pouco ("Madrugada", "Manhã", "Tarde", "Noite")
    distancia_km FLOAT,
    duracao_min FLOAT,
    duracao_transito_min FLOAT,
    diferenca_transito_min FLOAT,
    velocidade_media_kmh FLOAT,
    horario_pico BOOLEAN,
    origin VARCHAR(50),
    destination VARCHAR(50),
    start_lat FLOAT,
    start_lng FLOAT,
    end_lat FLOAT,
    end_lng FLOAT
    -- CONSTRAINT fk_raw_data FOREIGN KEY (raw_data_id) REFERENCES traffic_data (id) -- SUGESTÃO: Se traffic_data tiver um 'id'
);

-- Tabela para resumos
CREATE TABLE IF NOT EXISTS traffic_summary (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total_registros INTEGER,
    periodo_inicio TIMESTAMP WITH TIME ZONE,
    periodo_fim TIMESTAMP WITH TIME ZONE,
    media_duracao FLOAT,
    media_duracao_transito FLOAT,
    max_duracao FLOAT,
    min_duracao FLOAT,
    media_velocidade FLOAT,
    pior_horario VARCHAR(10),
    melhor_horario VARCHAR(10)
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_traffic_data_transformed_timestamp 
ON traffic_data_transformed(timestamp);

CREATE INDEX IF NOT EXISTS idx_traffic_data_transformed_data 
ON traffic_data_transformed(data);

CREATE INDEX IF NOT EXISTS idx_traffic_data_transformed_faixa_horario 
ON traffic_data_transformed(faixa_horario);

CREATE INDEX IF NOT EXISTS idx_traffic_summary_timestamp 
ON traffic_summary(timestamp); 