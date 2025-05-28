import pandas as pd
from datetime import datetime # Não mais usado para datetime.now aqui
import pytz # Para timezones
import numpy as np # Para np.nan em caso de divisão por zero
import logging

log = logging.getLogger(__name__)

def transform_traffic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma os dados brutos de trânsito adicionando dimensões úteis.
    Assume que o DataFrame de entrada 'df' tem uma coluna 'timestamp'
    com strings ISO formatadas em UTC.
    """
    if 'timestamp' not in df.columns:
        log.error("Coluna 'timestamp' não encontrada no DataFrame.")
        # Retornar DataFrame vazio ou levantar erro, dependendo da estratégia
        return pd.DataFrame()

    # Converte timestamp (string UTC) para datetime objects (timezone-aware UTC)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.tz_localize('UTC')
    
    # Remove linhas onde o timestamp não pôde ser convertido
    df.dropna(subset=['timestamp'], inplace=True)
    if df.empty:
        log.warning("DataFrame vazio após conversão e remoção de NaT em timestamps.")
        return df

    # Converte para timezone de São Paulo para features locais
    tz_sp = pytz.timezone('America/Sao_Paulo')
    df['timestamp_local'] = df['timestamp'].dt.tz_convert(tz_sp)

    # Extrai dimensões de tempo a partir do timestamp_local
    df['data'] = df['timestamp_local'].dt.date
    df['hora'] = df['timestamp_local'].dt.hour
    df['minuto'] = df['timestamp_local'].dt.minute
    df['dia_semana'] = df['timestamp_local'].dt.day_name(locale='pt_BR.utf8') # Exemplo com PT-BR
    df['dia_semana_num'] = df['timestamp_local'].dt.dayofweek # Segunda=0, Domingo=6

    # Cria faixas de horário
    df['faixa_horario'] = pd.cut(
        df['hora'],
        bins=[-1, 5, 11, 17, 23], # Ajustado para incluir 00:00 e 23:00
        labels=['Madrugada', 'Manhã', 'Tarde', 'Noite'],
        # include_lowest=True # Redundante com bins ajustados
        right=True # [0,6) -> (0,6] se right=True e include_lowest=True
    )

    # Calcula métricas adicionais
    df['distancia_km'] = df['distance_meters'] / 1000
    df['duracao_min'] = df['duration_seconds'] / 60
    df['duracao_transito_min'] = df['duration_in_traffic_seconds'] / 60

    # Calcula diferença entre duração normal e com trânsito
    df['diferenca_transito_min'] = df['duracao_transito_min'] - df['duracao_min']

    # Calcula velocidade média (km/h) com tratamento para divisão por zero
    # (duracao_min / 60) é a duração em horas
    df['velocidade_media_kmh'] = np.where(
        df['duracao_min'] > 0,
        df['distancia_km'] / (df['duracao_min'] / 60),
        0  # Ou np.nan se preferir
    )

    # Identifica horários de pico
    # Ajuste conforme sua definição de "pico"
    df['horario_pico'] = df['faixa_horario'].isin(['Manhã', 'Tarde']) & \
                         df['dia_semana_num'].isin(range(0, 5)) # Segunda a Sexta

    return df

def get_traffic_summary(df: pd.DataFrame) -> dict:
    """
    Gera um resumo estatístico dos dados de trânsito transformados.
    """
    if df.empty:
        log.warning("DataFrame vazio para gerar resumo. Retornando resumo vazio.")
        return {
            'total_registros': 0,
            'periodo_inicio': None,
            'periodo_fim': None,
            # ... outros campos com valores padrão
        }
    
    # Usa 'timestamp' (UTC) para periodo_inicio/fim para consistência
    summary = {
        'total_registros': len(df),
        'periodo_inicio': df['timestamp'].min().isoformat() if not df['timestamp'].empty else None,
        'periodo_fim': df['timestamp'].max().isoformat() if not df['timestamp'].empty else None,
        'media_duracao_min': df['duracao_min'].mean(),
        'media_duracao_transito_min': df['duracao_transito_min'].mean(),
        'max_duracao_transito_min': df['duracao_transito_min'].max(),
        'min_duracao_min': df['duracao_min'].min(),
        'media_velocidade_kmh': df['velocidade_media_kmh'][df['velocidade_media_kmh'] > 0].mean(), # Média sem os zeros
        'pior_horario_faixa': df.groupby('faixa_horario')['duracao_transito_min'].mean().idxmax() if not df.empty else None,
        'melhor_horario_faixa': df.groupby('faixa_horario')['duracao_transito_min'].mean().idxmin() if not df.empty else None
    }
    return summary