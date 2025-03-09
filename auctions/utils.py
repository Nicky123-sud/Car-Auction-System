import requests
from django.conf import settings

def fetch_vehicle_history(vin):
    url = f"{settings.VEHICLE_HISTORY_API_URL}{vin}?apikey={settings.VEHICLE_HISTORY_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None
