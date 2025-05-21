import requests
from model.food import Food

class ApiClient:
    def __init__(self, app_id, api_key):
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    def get_nutrition(self, query):
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {"query": query}
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        foods = []
        for f in data.get("foods", []):
            food = Food(
                name=f['food_name'],
                calories=f['nf_calories'],
                proteins=f['nf_protein'],
                fats=f['nf_total_fat'],
                carbs=f['nf_total_carbohydrate']
            )
            foods.append(food)

        return foods