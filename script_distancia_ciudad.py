import requests

api_key = '5b3ce3597851110001cf6248d699eb49cea14e3daecfcc93936c6609'

def geocode_location(place_name):
    geocode_url = 'https://api.openrouteservice.org/geocode/search'
    params = {
        'api_key': api_key,
        'text': place_name,
        'size': 1
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()
    
    try:
        coords = data['features'][0]['geometry']['coordinates']  # [lon, lat]
        display_name = data['features'][0]['properties']['label']
        return coords, display_name
    except (KeyError, IndexError):
        print(f"No se pudo geocodificar: {place_name}")
        return None, None

def get_travel_info(origin_coords, destination_coords, origin_name, destination_name):
    directions_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        'coordinates': [origin_coords, destination_coords]
    }
    response = requests.post(directions_url, json=body, headers=headers)
    data = response.json()
    
    try:
        summary = data['routes'][0]['summary']
        duration = int(summary['duration'])  # en segundos
        distance_m = summary['distance']     # en metros
        distance_km = distance_m / 1000

        # Duración en h:m:s
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60

        # Combustible
        consumo_km_por_litro = 10
        precio_litro = 1300  # pesos chilenos
        litros = distance_km / consumo_km_por_litro
        costo_combustible = litros * precio_litro

        # Imprimir narrativa
        print("\n🗺️  Resumen del viaje:")
        print(f"Desde: {origin_name}")
        print(f"Hasta: {destination_name}")
        print(f"Distancia total: {distance_km:.2f} km")
        print(f"Duración estimada: {hours}h {minutes}m {seconds}s")
        print(f"Combustible estimado: {litros:.2f} litros")
        print(f"Valor estimado del combustible: ${costo_combustible:,.0f} CLP")

        print(f"""\n🚗 Vas a recorrer aproximadamente {int(distance_km)} km desde {origin_name} hasta {destination_name},
lo cual tomará unas {hours} horas y {minutes} minutos,
consumiendo cerca de {litros:.1f} litros de bencina de 95 octanos,
lo que costará alrededor de ${costo_combustible:,.0f} pesos chilenos.
¡Buen viaje!\n""")
        
    except (KeyError, IndexError):
        print("No se pudo obtener la información del viaje.")

# Bucle principal
while True:
    print("\n🔄 NUEVO VIAJE (presiona 'q' para salir)")
    origen_input = input("Ingresa el nombre del origen: ").strip()
    if origen_input.lower() == 'q':
        print("👋 ¡Hasta pronto!")
        break

    destino_input = input("Ingresa el nombre del destino: ").strip()
    if destino_input.lower() == 'q':
        print("👋 ¡Hasta pronto!")
        break

    origen_coords, origen_nombre = geocode_location(origen_input)
    destino_coords, destino_nombre = geocode_location(destino_input)

    if origen_coords and destino_coords:
        get_travel_info(origen_coords, destino_coords, origen_nombre, destino_nombre)
