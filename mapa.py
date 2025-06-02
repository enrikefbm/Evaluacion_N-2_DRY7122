import urllib.parse

api_key = "56261da219074557887a6e705eeb8828"

punto1 = {"lat": -33.4489, "lon": -70.6693}  # Santiago de Chile
punto2 = {"lat": -31.9710, "lon": -71.3540}  # Los Vilos

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

print("URL del mapa Santiago - Los Vilos con línea:")
print(url)
