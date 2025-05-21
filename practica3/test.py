import requests

app_id = "c16184db"  
api_key = "2d1cceec43dbc7ad79cfd208acfd4577"

url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
headers = {
    "x-app-id": app_id,
    "x-app-key": api_key,
    "Content-Type": "application/json"
}

payload = {
    "query": "1 apple, 200g chicken breast, 100g rice"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    print("=== Nutritional info ===")
    for food in data.get("foods", []):
        print(f"{food['food_name'].title()}:")
        print(f"  Calories: {food['nf_calories']} kcal")
        print(f"  Protein: {food['nf_protein']} g")
        print(f"  Fat: {food['nf_total_fat']} g")
        print(f"  Carbs: {food['nf_total_carbohydrate']} g")
        print()
else:
    print(f"Error: {response.status_code} - {response.text}")
