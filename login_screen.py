"""
NexPOS - Premium Giriş Ekranı
Koyu gradient sol panel, temiz form, mikro animasyonlar
"""
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QCheckBox, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor
from styles import COLORS, FONTS, ICONS
from widgets import InfoDialog, add_shadow
import database


class LoginScreen(QWidget):
    login_success = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 600)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SOL - Marka Paneli (Koyu Gradient) =====
        left = QFrame()
        left.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0.3,y2:1,
                    stop:0 #0F172A, stop:0.4 #1E1B4B, stop:1 #4F46E5);
            }
        """)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(60, 60, 60, 40)
        ll.setSpacing(12)
        ll.addStretch(1)

        # Logo - büyük ve dikkat çekici
        logo_frame = QHBoxLayout()
        logo_dot = QFrame()
        logo_dot.setFixedSize(48, 48)
        logo_dot.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #818CF8, stop:1 #4F46E5);
            border-radius: 14px;
        """)
        ld_ly = QVBoxLayout(logo_dot)
        ld_ly.setContentsMargins(0, 0, 0, 0)
        ld_lbl = QLabel("N")
        ld_lbl.setAlignment(Qt.AlignCenter)
        ld_lbl.setFont(QFont(FONTS['family'], 22, QFont.Bold))
        ld_lbl.setStyleSheet("color: white; background: transparent;")
        ld_ly.addWidget(ld_lbl)
        logo_frame.addWidget(logo_dot)
        logo_frame.addSpacing(12)

        logo = QLabel("NexPOS")
        logo.setFont(QFont(FONTS['family'], 38, QFont.Bold))
        logo.setStyleSheet("color: white; background: transparent; letter-spacing: 3px;")
        logo_frame.addWidget(logo)
        logo_frame.addStretch()
        ll.addLayout(logo_frame)

        ll.addSpacing(8)

        tagline = QLabel("Restoranınızı akıllıca yönetin.")
        tagline.setFont(QFont(FONTS['family'], FONTS['size_lg']))
        tagline.setStyleSheet("color: rgba(255,255,255,0.6); background: transparent;")
        ll.addWidget(tagline)

        ll.addSpacing(40)

        # Özellikler - modern kartlar
        features = [
            ("Hızlı sipariş yönetimi", "Her an kontrol sizde"),
            ("Anlık satış ve raporlama", "Gerçek zamanlı veriler"),
            ("Çoklu kullanıcı desteği", "Rol bazlı erişim"),
            ("Güvenli yetki sistemi", "Verileriniz güvende"),
        ]
        for title, desc in features:
            f_frame = QFrame()
            f_frame.setStyleSheet("""
                QFrame {
                    background: rgba(255,255,255,0.06);
                    border-radius: 12px;
                    border: none;
                }
            """)
            f_ly = QHBoxLayout(f_frame)
            f_ly.setContentsMargins(16, 12, 16, 12)
            f_ly.setSpacing(12)

            check = QLabel(ICONS['check'])
            check.setFont(QFont(FONTS['family'], 16, QFont.Bold))
            check.setStyleSheet("color: #818CF8; background: transparent;")
            check.setFixedWidth(24)

            text_col = QVBoxLayout()
            text_col.setSpacing(2)
            tx = QLabel(title)
            tx.setFont(QFont(FONTS['family'], FONTS['size_md'], QFont.Bold))
            tx.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")
            dx = QLabel(desc)
            dx.setFont(QFont(FONTS['family'], FONTS['size_xs']))
            dx.setStyleSheet("color: rgba(255,255,255,0.4); background: transparent;")
            text_col.addWidget(tx)
            text_col.addWidget(dx)

            f_ly.addWidget(check)
            f_ly.addLayout(text_col, 1)
            ll.addWidget(f_frame)
            ll.addSpacing(4)

        ll.addStretch(2)

        ver = QLabel("v3.2.0  |  2026 NexPOS Technologies")
        ver.setFont(QFont(FONTS['family'], FONTS['size_xs']))
        ver.setStyleSheet("color: rgba(255,255,255,0.25); background: transparent;")
        ll.addWidget(ver)

        main_layout.addWidget(left, 1)

        # ===== SAĞ - Login Formu =====
        right = QFrame()
        right.setStyleSheet(f"background-color: {COLORS['bg_white']};")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(80, 50, 80, 40)
        rl.setSpacing(8)

        # Sağ üst logo
        logo_row = QHBoxLayout()
        logo_small = QLabel("NexPOS")
        logo_small.setFont(QFont(FONTS['family'], 16, QFont.Bold))
        logo_small.setStyleSheet(f"color: {COLORS['primary']}; background: transparent;")
        logo_row.addWidget(logo_small)
        logo_row.addStretch()
        rl.addLayout(logo_row)

        rl.addStretch(1)

        # Hoş Geldiniz
        welcome = QLabel("Hoş Geldiniz")
        welcome.setFont(QFont(FONTS['family'], FONTS['size_xxl'], QFont.Bold))
        welcome.setStyleSheet(f"color: {COLORS['text_dark']}; background: transparent;")
        rl.addWidget(welcome)

        subtitle = QLabel("Hesabınıza giriş yaparak devam edin")
        subtitle.setFont(QFont(FONTS['family'], FONTS['size_md']))
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; background: transparent;")
        rl.addWidget(subtitle)

        rl.addSpacing(32)

        # E-Posta
        el = QLabel("E-Posta veya Telefon")
        el.setFont(QFont(FONTS['family'], FONTS['size_sm'], QFont.Bold))
        el.setStyleSheet(f"color: {COLORS['text_primary']}; background: transparent;")
        rl.addWidget(el)
        rl.addSpacing(4)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ornek@nexpos.com")
        self.email_input.setFixedHeight(50)
        self.email_input.setFont(QFont(FONTS['family'], FONTS['size_md']))
        rl.addWidget(self.email_input)

        rl.addSpacing(16)

        # Şifre
        pl = QLabel("Şifre")
        pl.setFont(QFont(FONTS['family'], FONTS['size_sm'], QFont.Bold))
        pl.setStyleSheet(f"color: {COLORS['text_primary']}; background: transparent;")
        rl.addWidget(pl)
        rl.addSpacing(4)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(50)
        self.password_input.setFont(QFont(FONTS['family'], FONTS['size_md']))
        self.password_input.returnPressed.connect(self._do_login)
        rl.addWidget(self.password_input)

        rl.addSpacing(8)

        # Beni hatırla + Şifremi unuttum
        rem_row = QHBoxLayout()
        self.remember_cb = QCheckBox("Beni hatırla")
        self.remember_cb.setStyleSheet("background: transparent;")
        forgot = QPushButton("Şifremi Unuttum")
        forgot.setCursor(Qt.PointingHandCursor)
        forgot.setStyleSheet(f"""
            QPushButton {{ border: none; color: {COLORS['primary']};
                font-size: {FONTS['size_sm']}px; background: transparent; font-weight: bold; }}
            QPushButton:hover {{ color: {COLORS['primary_dark']}; text-decoration: underline; }}
        """)
        forgot.clicked.connect(self._forgot_password)
        rem_row.addWidget(self.remember_cb)
        rem_row.addStretch()
        rem_row.addWidget(forgot)
        rl.addLayout(rem_row)

        rl.addSpacing(28)

        # GİRİŞ YAP butonu
        self.login_btn = QPushButton("GİRİŞ YAP")
        self.login_btn.setFixedHeight(54)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setFont(QFont(FONTS['family'], 15, QFont.Bold))
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {COLORS['primary_dark']}, stop:1 #312E81);
            }}
            QPushButton:pressed {{
                background: #312E81;
            }}
        """)
        self.login_btn.clicked.connect(self._do_login)
        add_shadow(self.login_btn, blur=24, offset_y=8, color=QColor(79, 70, 229, 80))
        rl.addWidget(self.login_btn)

        rl.addSpacing(20)

        rl.addStretch(2)

        main_layout.addWidget(right, 1)

    def _do_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if not email or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return
        user = database.authenticate_user(email, password)
        if user:
            self.login_success.emit(user)
        else:
            QMessageBox.critical(self, "Hata", "E-posta/telefon veya şifre hatalı!")

    def _forgot_password(self):
        dlg = InfoDialog(
            "Şifremi Unuttum",
            "Şifre sıfırlama talebi için lütfen sistem yöneticisi ile iletişime geçin.\n\n"
            "İletişim: destek@nexpos.com\nTelefon: 0850 XXX XX XX",
            COLORS['warning'],
            self
        )
        dlg.exec()
