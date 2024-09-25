from fastapi import FastAPI 
import requests
import jwt
from datetime import datetime

app = FastAPI()

# Variables pour suivre l'état
service_start_time = datetime.now()
request_count = 0

@app.get("/health")
def health_check():
    global request_count
    uptime = datetime.now() - service_start_time
    return {
        "status": "OK",
        "uptime": str(uptime),
        "requests_served": request_count,
        "message": "The service is healthy and running."
    }

EXTERNAL_API_URL = "https://ensagri-pprd.api.agriculture.gouv.fr/arpent-resultats-api/etablissements" #problème d'access
EXTERNAL_API_URL2= 'https://impactco2.fr/api/v1/chauffage'

@app.get("/data_gouv")
def get_data_gouv():
    try:
        response = requests.get(EXTERNAL_API_URL2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Gérer les erreurs
        return {"error": "Failed to retrieve data", "details": str(e)}
    
def create_access_token(input: dict) -> str :
    to_encode = input.copy()
    encoded_jwt = jwt.encode(to_encode, 'SECRET_KEY', )
    return encoded_jwt

# Endpoint pour générer le JWT
@app.post("/token")
def generate_jwt(name: dict):
    access_token = create_access_token(name)
    return {"access_token": access_token, "token_type": "bearer"}

# RESTE A CREER UNE FONCTION QUI UTILISE LE TOKEN avec jwt.decode

@app.get("/fonction")
def petite_fonction():
    data_dict=get_data_gouv()
    if 'data' in data_dict:
        ecv_values = [float(item['ecv']) for item in data_dict['data']]
        return sum(ecv_values) / len(ecv_values)
    else:
        return []  
