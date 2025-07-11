import os
import pandas as pd
from serpapi import Client
from dotenv import load_dotenv

load_dotenv()


class JobRadarScraper:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def buscar_vagas(self, query: str, location: str) -> pd.DataFrame:
        if not self.api_key:
            raise RuntimeError("Defina SERPAPI_KEY no .env ou variável de ambiente")

        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": self.api_key,
        }

        client = Client(api_key=self.api_key)
        try:
            results = client.search(params)
        except Exception as e:
            raise RuntimeError(f"Erro ao consultar a API: {e}")
        jobs = results.get("jobs_results", [])

        columns = ["Título", "Empresa", "Localização", "Link", "Descrição"]
        rows = []
        for job in jobs:
            rows.append(
                {
                    "Título": job.get("title", ""),
                    "Empresa": job.get("company_name", ""),
                    "Localização": job.get("location", ""),
                    "Link": job.get("link", ""),
                    "Descrição": job.get("description", "")[:300],
                }
            )
        df = pd.DataFrame(rows, columns=columns)
        return df
