from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QScrollArea, QCompleter, QListWidget, QToolBar, QMainWindow
)
from PyQt6.QtCore import Qt
import sys
from foodapi import ApiClient
from nutrition_widget import NutritionInfoWidget
from models import User, Meal, get_db  # Importăm clasele User și Meal, și funcția get_db()
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class NutritionApp(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.api_client = ApiClient("c16184db", "2d1cceec43dbc7ad79cfd208acfd4577")
        self.setWindowTitle("Food Tracker")
        self.setGeometry(100, 100, 800, 500)

        self.user = user
        self.user_id = user.id if user else None

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        toolbar = QToolBar("Toolbar")
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)
        meals_button = QPushButton("Meals")
        meals_button.clicked.connect(lambda: None)  # Placeholder
        toolbar.addWidget(meals_button)

        toolbar.addSeparator()
        toolbar.addSeparator()
        disc_button = QPushButton("Disconnect")
        disc_button.clicked.connect(self.open_startscreen_app)
        toolbar.addWidget(disc_button)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(12)

        left_layout.addWidget(QLabel("Food:"))
        self.food_input = QLineEdit()
        left_layout.addWidget(self.food_input)

        food_list = self.load_food_list("foods.txt")
        completer = QCompleter(food_list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.food_input.setCompleter(completer)

        left_layout.addWidget(QLabel("Weight (g):"))
        self.weight_input = QLineEdit()
        left_layout.addWidget(self.weight_input)

        self.button = QPushButton("Show nutrition stats")
        self.button.clicked.connect(self.show_nutrition)
        left_layout.addWidget(self.button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_container.setLayout(self.results_layout)
        self.scroll_area.setWidget(self.results_container)
        left_layout.addWidget(self.scroll_area)

        main_layout.addWidget(left_widget, 3)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(12)
        right_widget.setStyleSheet("background-color: #e6f0ff; border-radius: 12px;")

        label_foods = QLabel("Foods added:")
        label_foods.setStyleSheet("font-weight: 700; font-size: 18px; color: #2a5d9f;")
        right_layout.addWidget(label_foods)

        self.foods_list_widget = QListWidget()
        right_layout.addWidget(self.foods_list_widget)

        label_totals = QLabel("Totals:")
        label_totals.setStyleSheet("font-weight: 700; font-size: 18px; color: #2a5d9f;")
        right_layout.addWidget(label_totals)

        self.total_calories_label = QLabel("Calories: 0 kcal")
        self.total_proteins_label = QLabel("Proteins: 0 g")
        self.total_fats_label = QLabel("Fats: 0 g")
        self.total_carbs_label = QLabel("Carbs: 0 g")

        for lbl in [self.total_calories_label, self.total_proteins_label,
                    self.total_fats_label, self.total_carbs_label]:
            lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #2a5d9f;")
            right_layout.addWidget(lbl)

        main_layout.addWidget(right_widget, 2)

        self.setLayout(main_layout)

        self.all_foods = []

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f5;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                color: #333;
            }
            QLabel {
                font-weight: 600;
                color: #444;
            }
            QLineEdit {
                border: 2px solid #aaa;
                border-radius: 6px;
                padding: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3a8dde;
                background-color: #eaf4ff;
            }
            QPushButton {
                background-color: #3a8dde;
                color: white;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2f6cbf;
            }
            QPushButton:pressed {
                background-color: #255190;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 5px;
            }
            QScrollArea {
                border: none;
            }
        """)

        button_style = """
            QPushButton {
                background-color: #2a5d9f;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1d4e89;
            }
        """
        self.button.setStyleSheet(button_style)

        savemeal_button = QPushButton("Save Meal")
        savemeal_button.setStyleSheet(button_style)
        savemeal_button.clicked.connect(self.save_meal)
        right_layout.addWidget(savemeal_button)

    def open_startscreen_app(self):
        from startscreen import StartScreen
        self.start_screen = StartScreen()
        self.start_screen.show()
        self.close()

    def show_nutrition(self):
        food = self.food_input.text().strip()
        weight = self.weight_input.text().strip()

        if not food:
            QMessageBox.warning(self, "Warning", "Please enter a food item.")
            return
        if not weight.isdigit():
            QMessageBox.warning(self, "Warning", "Please enter a valid weight in grams (number).")
            return

        query = f"{weight}g {food}"
        try:
            foods = self.api_client.get_nutrition(query)
            if not foods:
                self.clear_results()
                QMessageBox.information(self, "Info", "No nutrition data found.")
                return

            self.clear_results()
            for food_item in foods:
                widget = NutritionInfoWidget(food_item)
                self.results_layout.addWidget(widget)
                self.all_foods.append(food_item)
                list_item_text = f"{food_item.name.title()} - {weight} g"
                self.foods_list_widget.addItem(list_item_text)

            self.update_totals()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def update_totals(self):
        total_cal = sum(f.calories for f in self.all_foods)
        total_prot = sum(f.proteins for f in self.all_foods)
        total_fat = sum(f.fats for f in self.all_foods)
        total_carb = sum(f.carbs for f in self.all_foods)

        self.total_calories_label.setText(f"Calories: {total_cal:.2f} kcal")
        self.total_proteins_label.setText(f"Proteins: {total_prot:.2f} g")
        self.total_fats_label.setText(f"Fats: {total_fat:.2f} g")
        self.total_carbs_label.setText(f"Carbs: {total_carb:.2f} g")

    def clear_results(self):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_food_list(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                foods = [line.strip() for line in f if line.strip()]
            return foods
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not load food list from {filename}.\n{e}")
            return []

    def save_meal(self):
        if not self.all_foods:
            QMessageBox.warning(self, "Warning", "No foods to save.")
            return

        db: Session = next(get_db())  # Get a SQLAlchemy Session
        try:
            for food in self.all_foods:
                # Create a new Meal object
                new_meal = Meal(
                    user_id=self.user_id,
                    food_name=food.name,
                    calories=food.calories,
                    proteins=food.proteins,
                    fats=food.fats,
                    carbs=food.carbs
                )
                db.add(new_meal)  # Add the Meal object to the session
            db.commit()  # Commit the transaction to save all meals

            QMessageBox.information(self, "Success", "Meal saved successfully.")
            self.all_foods.clear()
            self.foods_list_widget.clear()
            self.clear_results()
            self.update_totals()
        except SQLAlchemyError as e:
            db.rollback()  # Rollback the transaction in case of an error
            QMessageBox.critical(self, "Database Error", f"Could not save meal:\n{e}")
        finally:
            db.close()  # Ensure the session is closed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NutritionApp()
    window.show()
    sys.exit(app.exec())
