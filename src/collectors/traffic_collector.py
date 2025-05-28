import os
# import time # Não utilizado diretamente
from datetime import datetime
import googlemaps
from dotenv import load_dotenv
# from collectors.db_utils import insert_traffic_data # Importado na DAG
import psycopg2 # Ainda usado em db_utils, mas não diretamente aqui
# import json # Não utilizado diretamente aqui
import logging
import pytz # Para timezones

# Carrega as variáveis de ambiente
load_dotenv()
log = logging.getLogger(__name__)

def clean_env_value(value):
    """Limpa o valor da variavel de ambiente, removendo comentários e espaços"""
    if value:
        return value.split('#')[0].strip()
    return None

def get_traffic_data():
    """
    Coleta dados de trânsito entre Ponta Grossa e Curitiba usando Google Maps API.
    Retorna os dados em UTC.
    """
    log.info("=== INÍCIO DA COLETA DE DADOS ===")

    # Inicializa o cliente do Google Maps
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        log.error("GOOGLE_MAPS_API_KEY não definida.")
        return None
    gmaps = googlemaps.Client(key=api_key)

    # Coordenadas de origem e destino
    try:
        origin_lat = float(clean_env_value(os.getenv('ORIGIN_LAT')))
        origin_lng = float(clean_env_value(os.getenv('ORIGIN_LNG')))
        destination_lat = float(clean_env_value(os.getenv('DESTINATION_LAT')))
        destination_lng = float(clean_env_value(os.getenv('DESTINATION_LNG')))
    except (TypeError, ValueError) as e:
        log.error(f"Erro ao converter coordenadas para float: {e}")
        return None

    origin = (origin_lat, origin_lng)
    destination = (destination_lat, destination_lng)
    
    current_time_utc = datetime.now(pytz.utc) # Usar UTC

    try:
        log.info("Consultando Google Maps API...")
        directions_result = gmaps.directions(
            origin,
            destination,
            mode="driving",
            departure_time=current_time_utc, # Usar current_time_utc para departure_time
            traffic_model="best_guess"
        )

        if directions_result:
            route = directions_result[0]
            leg = route['legs'][0]

            traffic_data = {
                'timestamp': current_time_utc.isoformat(), # Timestamp da coleta em UTC
                'origin': str('Ponta Grossa'),
                'destination': str('Curitiba'),
                'distance_meters': int(leg['distance']['value']),
                'duration_seconds': int(leg['duration']['value']),
                'duration_in_traffic_seconds': int(leg.get('duration_in_traffic', {}).get('value', 0)),
                'start_location': {
                    'lat': float(leg['start_location']['lat']),
                    'lng': float(leg['start_location']['lng'])
                },
                'end_location': {
                    'lat': float(leg['end_location']['lat']),
                    'lng': float(leg['end_location']['lng'])
                }
            }

            log.info("Resumo dos dados coletados:")
            log.info(f"Distancia: {traffic_data['distance_meters']/1000:.2f} km")
            log.info(f"Duracao: {traffic_data['duration_seconds']/60:.2f} minutos")
            if traffic_data['duration_in_traffic_seconds']:
                log.info(f"Duracao com transito: {traffic_data['duration_in_traffic_seconds']/60:.2f} minutos")

            return traffic_data

    except googlemaps.exceptions.ApiError as e:
        log.error(f"Erro na API do Google Maps: {e}")
    except Exception as e:
        log.error(f"Erro inesperado ao coletar dados: {e}", exc_info=True)
    
    return None

if __name__ == "__main__":
    # Para fins de teste local do coletor
    # Note que insert_traffic_data precisaria ser importado e chamado aqui se desejado.
    # from collectors.db_utils import insert_traffic_data # Exemplo
    logging.basicConfig(level=logging.INFO)
    log.info("Iniciando coleta de dados de transito (teste local)...")
    data = get_traffic_data()
    if data:
        log.info("Dados coletados (teste local):")
        import json
        log.info(json.dumps(data, indent=4))
        # Se quiser salvar no banco durante o teste local:
        # from collectors.db_utils import insert_traffic_data
        # log.info("Salvando dados no banco (teste local)...")
        # insert_traffic_data(data)
        # log.info("Dados salvos com sucesso (teste local)!")
    else:
        log.info("Nenhum dado retornado pela API (teste local).")