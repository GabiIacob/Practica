import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemplu Simplu PyQt6")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Introdu ceva:")
        layout.addWidget(self.label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        self.button = QPushButton("Arata mesaj")
        self.button.clicked.connect(self.show_message)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_message(self):
        text = self.text_input.text()
        QMessageBox.information(self, "Mesaj", f"Ai scris: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())
