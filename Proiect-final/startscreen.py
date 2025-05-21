from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from controllers.main import NutritionApp
import hashlib
from model.models import User, get_db, Base 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import sys
from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Food Tracker")
        self.setGeometry(100, 100, 400, 500)
        self.setFixedSize(400, 500)

        engine = create_engine("sqlite:///users.db")  

        Base.metadata.create_all(engine) 

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        label_font = QFont("Segoe UI", 10)
        input_font = QFont("Segoe UI", 10)
        btn_font = QFont("Segoe UI", 11, QFont.Weight.Bold)

        for label_text, field in [("Name:", "name_input"), ("Email:", "email_input"), ("Password:", "password_input")]:
            label = QLabel(label_text)
            label.setFont(label_font)
            layout.addWidget(label)

            line_edit = QLineEdit()
            line_edit.setFont(input_font)
            line_edit.setFixedHeight(36)
            line_edit.setStyleSheet("padding: 6px; border: 1px solid gray; border-radius: 6px;")
            setattr(self, field, line_edit)
            layout.addWidget(line_edit)

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        btn_sign_in = QPushButton("Sign In")
        btn_login = QPushButton("Login")
        btn_use_without_account = QPushButton("Use Without Account")

        for btn in (btn_sign_in, btn_login, btn_use_without_account):
            btn.setFont(btn_font)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a5d9f;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #1f4a80;
                }
                QPushButton:pressed {
                    background-color: #163a61;
                }
            """)
            btn.setFixedHeight(44)
            layout.addWidget(btn)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.setLayout(layout)

        btn_sign_in.clicked.connect(self.sign_in)
        btn_login.clicked.connect(self.login)
        btn_use_without_account.clicked.connect(self.use_without_account)

    def hash_password(self, text):
        sha256 = hashlib.sha256()
        sha256.update(text.encode('utf-8'))
        return sha256.hexdigest()

    def sign_in(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        hashed_password = self.hash_password(password)

        db: Session = next(get_db())
        try:
            new_user = User(name=name, email=email, password=hashed_password)
            db.add(new_user)
            db.commit()
            QMessageBox.information(self, "Success", "Account created successfully.")
        except IntegrityError:
            db.rollback()
            QMessageBox.warning(self, "Error", "User with this name or email already exists.")
        finally:
            db.close()

    def login(self):
        name = self.name_input.text()
        password = self.password_input.text()

        if not name or not password:
            QMessageBox.warning(self, "Input Error", "Name and password are required.")
            return

        hashed_password = self.hash_password(password)

        db: Session = next(get_db())
        try:
            user_data = db.query(User).filter(User.name == name, User.password == hashed_password).first()

            if user_data:
                self.current_user_obj = user_data
                QMessageBox.information(self, "Login", "Login successful!")
                self.open_nutrition_app()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
        finally:
            db.close()

    def use_without_account(self):
        self.current_user_obj = None
        self.open_nutrition_app()

    def open_nutrition_app(self):
        self.nutrition_app = NutritionApp(user=self.current_user_obj)
        self.nutrition_app.show()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_screen = StartScreen()
    start_screen.show()
    sys.exit(app.exec())
