from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QSizePolicy, 
    QSpacerItem, QMessageBox
)
from PyQt6.QtCore import Qt, QRectF, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from model.models import Meal
from sqlalchemy.orm import Session
from model.models import get_db
from datetime import timedelta


class MealHistoryWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Meal History")
        self.setGeometry(200, 200, 650, 500)

        main_layout = QVBoxLayout(self)

        title_label = QLabel("Your Meal History")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #2a5d9f;
            margin-bottom: 15px;
        """)
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        self.container = QWidget()
        scroll.setWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(15)

        self.load_meals()

    def load_meals(self):
        db: Session = next(get_db())
        try:
            meals = db.query(Meal).filter(Meal.user_id == self.user_id).order_by(Meal.created_at.asc()).all()
            if not meals:
                self.container_layout.addWidget(QLabel("No meals found."))
                return

            meals_by_group = self.group_meals_by_time(meals, max_interval_minutes=60)

            for group_id, meals_list in sorted(meals_by_group.items()):
                self.container_layout.addWidget(self._create_meal_section(group_id, meals_list))

            spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.container_layout.addItem(spacer)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load meals:\n{e}")
        finally:
            db.close()

    def group_meals_by_time(self, meals, max_interval_minutes=60):
        grouped = {}
        current_group_id = 1
        if not meals:
            return grouped
        
        grouped[current_group_id] = [meals[0]]
        last_time = meals[0].created_at

        for meal in meals[1:]:
            if (meal.created_at - last_time) <= timedelta(minutes=max_interval_minutes):
                grouped[current_group_id].append(meal)
            else:
                current_group_id += 1
                grouped[current_group_id] = [meal]
            last_time = meal.created_at
        
        return grouped

    def _create_meal_section(self, meal_num, meals):
        meal_frame = QFrame()
        meal_frame.setStyleSheet("""
            QFrame {
                background-color: #dce6f7;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(meal_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        meal_label = QLabel(f"Masa {meal_num}")
        meal_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1f3b73;
            margin-bottom: 10px;
        """)
        layout.addWidget(meal_label)

        # Calcul total nutrienti
        total_proteins = sum(m.proteins for m in meals)
        total_carbs = sum(m.carbs for m in meals)
        total_fats = sum(m.fats for m in meals)

        # Creează un widget custom pentru pie chart direct aici
        pie_chart = PieChartWidget(total_proteins, total_carbs, total_fats)
        layout.addWidget(pie_chart, alignment=Qt.AlignmentFlag.AlignCenter)

        for meal in meals:
            layout.addWidget(self._create_food_item(meal))

        return meal_frame

    def _create_food_item(self, meal):
        food_frame = QFrame()
        food_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #bbb;
            }
            QFrame:hover {
                background-color: #f0f5ff;
                border-color: #3a8dde;
            }
        """)
        layout = QHBoxLayout(food_frame)
        layout.setContentsMargins(8, 8, 8, 8)

        name_label = QLabel(meal.food_name.title())
        name_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #222;")
        layout.addWidget(name_label, stretch=1)

        nutrition_label = QLabel(
            f"Cal: {meal.calories:.0f} kcal | Prot: {meal.proteins:.1f} g | "
            f"Fats: {meal.fats:.1f} g | Carb: {meal.carbs:.1f} g"
        )
        nutrition_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(nutrition_label)

        return food_frame


class PieChartWidget(QFrame):
    def __init__(self, proteins, carbs, fats, parent=None):
        super().__init__(parent)
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats
        self.setMinimumSize(120, 120)
        self.setMaximumSize(120, 120)
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        total = self.proteins + self.carbs + self.fats
        if total == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

        start_angle = 0

        def draw_segment(value, color):
            nonlocal start_angle
            span_angle = int(360 * (value / total))
            painter.setBrush(QColor(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, start_angle * 16, span_angle * 16)
            start_angle += span_angle

        draw_segment(self.proteins, '#3a86ff')  # albastru - proteine
        draw_segment(self.carbs, '#ffbe0b')     # galben - carbohidrati
        draw_segment(self.fats, '#fb5607')      # portocaliu - grasimi

        # Text in centru (total kcal)
        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        kcal = int(self.proteins * 4 + self.carbs * 4 + self.fats * 9)
        text = f"{kcal} kcal"
        text_rect = painter.fontMetrics().boundingRect(text)
        x = (self.width() - text_rect.width()) / 2
        y = (self.height() + text_rect.height()) / 2 - 10
        painter.drawText(int(x), int(y), text)
