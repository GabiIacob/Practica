class Food:
    def __init__(self, name, calories, proteins, carbs, fats):
        self.name = name
        self.calories = calories
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats

    def __str__(self):
        return (f"{self.name.title()}:\n"
                f" Calories: {self.calories} kcal\n"
                f" Proteins: {self.proteins} g\n"
                f" Fats: {self.fats} g\n"
                f" Carbs: {self.carbs} g\n")