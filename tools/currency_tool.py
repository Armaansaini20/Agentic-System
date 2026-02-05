import requests
import os
from .base import BaseTool

class CurrencyTool(BaseTool):
    def execute(self, from_code, to_code, amount):
        api_key = os.getenv("EXCHANGE_RATE_KEY")
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_code}/{to_code}/{amount}"
        
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("result") == "success":
                return {
                    "conversion": f"{amount} {from_code} = {data['conversion_result']} {to_code}",
                    "rate": data["conversion_rate"]
                }
            return {"error": "Invalid currency codes or API error"}
        except Exception as e:
            return {"error": str(e)}

    def get_definition(self):
        return {
            "name": "currency_tool",
            "description": "Convert an amount from one currency to another (e.g., USD to INR).",
            "parameters": {
                "from_code": "string (3-letter code)",
                "to_code": "string (3-letter code)",
                "amount": "number"
            }
        }