import requests
import math
import urllib.parse

# Constantes
SANTIAGO_LAT = -33.4489
SANTIAGO_LON = -70.6693
API_KEY = "56261da219074557887a6e705eeb8828"

def obtener_info_ip(ip):
    url = f"https://ipapi.co/{ip}/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error al hacer la solicitud a ipapi.co:", e)
        return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def generar_url_mapa(punto1, punto2, api_key):
    center_lat = (punto1["lat"] + punto2["lat"]) / 2
    center_lon = (punto1["lon"] + punto2["lon"]) / 2
    width = 800
    height = 600
    zoom = 7

    path_value = f"weight:4|color:0x0000ff|{punto1['lon']},{punto1['lat']}|{punto2['lon']},{punto2['lat']}"
    path_encoded = urllib.parse.quote(path_value, safe='|:,')

    url = (
        f"https://maps.geoapify.com/v1/staticmap?"
        f"style=osm-carto&width={width}&height={height}"
        f"&center=lonlat:{center_lon},{center_lat}&zoom={zoom}"
        f"&marker=lonlat:{punto1['lon']},{punto1['lat']};color:%23ff0000;size:medium"
        f"&marker=lonlat:{punto2['lon']},{punto2['lat']};color:%230000ff;size:medium"
        f"&path={path_encoded}"
        f"&apiKey={api_key}"
    )
    return url

def main():
    ip_usuario = input("Ingresa la IP del DNS que deseas consultar: ").strip()
    info = obtener_info_ip(ip_usuario)
    if not info:
        print("No se pudo obtener información de la IP.")
        return
    
    lat = info.get('latitude')
    lon = info.get('longitude')

    if lat is None or lon is None:
        print("No se pudo obtener coordenadas de la IP.")
        return
    
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        print("Coordenadas no válidas.")
        return

    distancia = calcular_distancia(SANTIAGO_LAT, SANTIAGO_LON, lat, lon)
    print(f"Distancia aproximada entre Santiago y la IP: {distancia:.2f} km")

    punto_santiago = {"lat": SANTIAGO_LAT, "lon": SANTIAGO_LON}
    punto_ip = {"lat": lat, "lon": lon}

    url_mapa = generar_url_mapa(punto_santiago, punto_ip, API_KEY)
    print("\nURL del mapa con Santiago y ubicación de la IP:")
    print(url_mapa)

if __name__ == "__main__":
    main()
