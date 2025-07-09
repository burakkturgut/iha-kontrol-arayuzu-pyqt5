import sys
import json
import os
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İSTİKBAL İHA KULLANICI GİRİŞİ")
        self.setGeometry(600, 300, 350, 250)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QPushButton {
                background-color: #0078d7;
                border: none;
                padding: 8px;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Takım logosu (giriş ekranı üst kısmında)
        self.logo_label = QLabel()
        pixmap = QPixmap("istikbal.png")  # 📸 görsel dosyasının adını buraya yaz
        self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        self.user_label = QLabel("👤 Kullanıcı Adı:")
        self.user_input = QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        self.pass_label = QLabel("🔒 Şifre:")
        pw_layout = QHBoxLayout()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.toggle_password_btn = QPushButton("👁️")
        self.toggle_password_btn.setFixedWidth(30)
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        pw_layout.addWidget(self.pass_input)
        pw_layout.addWidget(self.toggle_password_btn)
        layout.addWidget(self.pass_label)
        layout.addLayout(pw_layout)


        self.login_button = QPushButton("🔓 Giriş Yap")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        try:
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
                for user in users:
                    if user["username"] == username and user["password"] == password:
                        self.accept_login()
                        return
                QMessageBox.warning(self, "Hatalı Giriş", "Kullanıcı adı veya şifre yanlış!")
        except FileNotFoundError:
            QMessageBox.critical(self, "Hata", "users.json dosyası bulunamadı!")

    def accept_login(self):
        from main import IHAKontrolArayuzu  # senin asıl arayüz sınıfın
        self.hide()
        self.ana_pencere = IHAKontrolArayuzu()
        self.ana_pencere.show()

    def toggle_password_visibility(self):
        if self.toggle_password_btn.isChecked():
            self.pass_input.setEchoMode(QLineEdit.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
