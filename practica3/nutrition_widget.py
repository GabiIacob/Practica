from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class NutritionInfoWidget(QWidget):
    def __init__(self, food):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        self.setStyleSheet("""
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 8px;
        """)

        name_label = QLabel(food.name.title())
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-weight: 700; font-size: 18px; color: #333;")
        layout.addWidget(name_label)

        def create_nutrition_row(icon_path, text):
            row = QHBoxLayout()
            row.setSpacing(10)
            
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            row.addWidget(icon_label)
            
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 14px; color: #555;")
            text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(text_label)
            
            row.addStretch()
            return row

        layout.addLayout(create_nutrition_row("calories.png", f"{food.calories} kcal"))
        layout.addLayout(create_nutrition_row("proteins.png", f"{food.proteins} g Proteins"))
        layout.addLayout(create_nutrition_row("fat.png", f"{food.fats} g Fats"))
        layout.addLayout(create_nutrition_row("carbs.png", f"{food.carbs} g Carbs"))

        self.setLayout(layout)
