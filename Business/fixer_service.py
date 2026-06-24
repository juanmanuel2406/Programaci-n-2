import os
import requests
from dotenv import load_dotenv

class FixerService:

    def __init__(self):
        _base_dir = os.path.dirname(os.path.abspath(__file__))
        _env_path = os.path.join(_base_dir, "..", "Data", ".env")
        if os.path.exists(_env_path):
            load_dotenv(_env_path)
        self.api_key = os.getenv("FIXER_API_KEY", "4f73f7de235a09288e8c1988da9b6fcf")
        self.base_url = "http://data.fixer.io/api"

    def get_rates(self, symbols="USD,ARS,EUR"):
        url = "{}/latest?access_key={}&symbols={}".format(self.base_url, self.api_key, symbols)
        resp = requests.get(url)
        data = resp.json()
        if not data.get("success"):
            raise Exception("Error al obtener cotizaciones de Fixer.io")
        return data["rates"]
