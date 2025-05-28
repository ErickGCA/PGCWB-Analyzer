import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
ORIGIN = f"{os.getenv('ORIGIN_LAT')},{os.getenv('ORIGIN_LNG')}"
DESTINATION = f"{os.getenv('DESTINATION_LAT')},{os.getenv('DESTINATION_LNG')}"

def get_route():
    url = f"https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    body = {
        "origin": {"location": {"latLng": {"latitude": float(os.getenv('ORIGIN_LAT')), "longitude": float(os.getenv('ORIGIN_LNG'))}}},
        "destination": {"location": {"latLng": {"latitude": float(os.getenv('DESTINATION_LAT')), "longitude": float(os.getenv('DESTINATION_LNG'))}}},
        "travelMode": "DRIVE"
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        print("Resposta da API:")
        print(data)
        if "routes" in data and len(data["routes"]) > 0:
            route = data["routes"][0]
            print(f"Distância: {route['distanceMeters']/1000:.2f} km")
            print(f"Duração: {int(route['duration'].replace('s', ''))/60:.2f} minutos")
        else:
            print("Nenhuma rota encontrada.")
    else:
        print("Erro na requisição:", response.status_code, response.text)

if __name__ == "__main__":
    get_route()