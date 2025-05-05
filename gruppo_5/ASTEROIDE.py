import requests

API_KEY = "*****"
URL = "https://api.nasa.gov/neo/rest/v1/feed"

# Ottenere i dati sugli asteroidi
response = requests.get(f"{URL}?api_key={API_KEY}")

if response.ok:
    data = response.json()
    asteroidi = []
    
    for giorno in data["near_earth_objects"]:
        asteroidi.extend(data["near_earth_objects"][giorno])
    
    # Livello 1: Conta degli asteroidi pericolosi e non
    pericolosi = sum(1 for a in asteroidi if a["is_potentially_hazardous_asteroid"])
    innocui = len(asteroidi) - pericolosi
    print(f"Asteroidi pericolosi: {pericolosi}")
    print(f"Asteroidi innocui: {innocui}")
    
    # Livello 2: Filtrare asteroidi per raggio minimo
    raggio_min = float(input("Inserisci un raggio minimo in metri: ")) / 1000  # Convertiamo in km
    grandi_asteroidi = [
        (a["name"], a["estimated_diameter"]["kilometers"]["estimated_diameter_min"], a["estimated_diameter"]["kilometers"]["estimated_diameter_max"])
        for a in asteroidi if a["estimated_diameter"]["kilometers"]["estimated_diameter_min"] > raggio_min
    ]
    
    if grandi_asteroidi:
        print("Asteroidi più grandi del raggio minimo:")
        for nome, r_min, raggio_max in grandi_asteroidi:
            print(f"{nome}: {r_min:.3f} km - {raggio_max:.3f} km")
    else:
        print("Nessun asteroide supera il raggio indicato.")
else:
    print("Errore!", response.reason)
