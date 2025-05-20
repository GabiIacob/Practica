from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_models_file import Base, Meal  

engine = create_engine('sqlite:///meal.db')
Base.metadata.create_all(engine) 

Session = sessionmaker(bind=engine)
session = Session()
new_meal = Meal(
    user_id=1,  
    food_name="Chicken Salad",
    calories=350,
    proteins=30,
    fats=10,
    carbs=20
)
session.add(new_meal)
session.commit()