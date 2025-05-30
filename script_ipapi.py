import requests
import math

# Coordenadas de Santiago, Chile
SANTIAGO_LAT = -33.4489
SANTIAGO_LON = -70.6693

def obtener_info_ip(ip):
    url = f"https://ipapi.co/{ip}/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print("Error al hacer la solicitud:", e)
        return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

# Solicitar IP al usuario
ip_usuario = input("🔎 Ingresa la IP del DNS que deseas consultar: ").strip()

# Obtener y mostrar información
info = obtener_info_ip(ip_usuario)

if info:
    print("\n📡 Información de la IP consultada:")
    print(f"IP: {info.get('ip')}")
    print(f"País: {info.get('country_name')}")
    print(f"Ciudad: {info.get('city')}")
    print(f"Región: {info.get('region')}")
    print(f"Organización: {info.get('org')}")
    print(f"ASN: {info.get('asn')}")
    lat = info.get('latitude')
    lon = info.get('longitude')

    if lat is not None and lon is not None:
        try:
            lat = float(lat)
            lon = float(lon)
            distancia_km = calcular_distancia(SANTIAGO_LAT, SANTIAGO_LON, lat, lon)
            print(f"📏 Distancia aproximada a Santiago, Chile: {distancia_km:.2f} km")
        except ValueError:
            print("⚠️ Error al procesar las coordenadas.")
    else:
        print("⚠️ No se pudo obtener coordenadas geográficas para calcular distancia.")
else:
    print("❌ No se pudo obtener la información de la IP.")
