import requests

STAC_API_URL = "https://data.inpe.br/bdc/stac/v1"

params = {
    "collections": ["AMZ1-WFI-L4-SR-1"],
    "bbox": [
        -60.5000,  # longitude mínima (Oeste)
        -3.3000,   # latitude mínima (Sul)
        -59.5000,  # longitude máxima (Leste)
        -2.3000    # latitude máxima (Norte)
    ],
    "datetime": "2025-04-03/2025-05-03",
    "limit": 3
}

response = requests.post(f"{STAC_API_URL}/search", json=params)

if response.status_code == 200:
    data = response.json()
    features = data.get("features", [])
    print(f"Total de imagens encontradas: {len(features)}\n")

    for item in features:
        print(f"ID: {item['id']}")
        banda_4_keys = [k for k in item['assets'].keys() if 'BAND4' in k.upper()]
        
        if banda_4_keys:
            for key in banda_4_keys:
                print(f"Banda 4 ({key}): {item['assets'][key]['href']}")
        else:
            print("Banda 4 não encontrada.")
        
        print("-" * 60)
else:
    print(f"Erro {response.status_code}: {response.text}")
