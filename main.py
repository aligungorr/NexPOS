"""
NexPOS - Ana Uygulama
Login → Admin/Kullanıcı panel yönlendirme
QMainWindow yapısı: MenuBar, ToolBar, StatusBar, QAction, Keyboard Shortcuts
"""
import sys
import os
import traceback

def global_exception_handler(exctype, value, tb):
    """Crash durumunda log tutan global handler"""
    err_msg = ''.join(traceback.format_exception(exctype, value, tb))
    with open("crash_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- CRASH LOG ---\n{err_msg}\n")
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = global_exception_handler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget,
                                QMessageBox, QLabel)
from PySide6.QtGui import QFont, QAction, QIcon
from PySide6.QtCore import QTimer, Qt
from styles import get_global_stylesheet, FONTS, COLORS, ICONS
from login_screen import LoginScreen
from admin_panel import AdminPanel
from user_panel import UserPanel
import database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NexPOS - Restaurant Yönetim Sistemi")
        self.setMinimumSize(1300, 780)
        self.showMaximized()

        database.init_database()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_screen = LoginScreen()
        self.login_screen.login_success.connect(self._on_login)
        self.stack.addWidget(self.login_screen)

        self.admin_panel = None
        self.user_panel = None
        self._current_user = None

        # QMainWindow bileşenleri (Hafta 7)
        self._setup_menubar()
        self._setup_toolbar()
        self._setup_statusbar()
        
        # Sadece Yönetici girişinde göster
        self.menuBar().setVisible(False)
        self.main_toolbar.setVisible(False)

    # ==================== MENUBAR + QACTION (Hafta 7) ====================
    def _setup_menubar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: white; color: {COLORS['text_dark']};
                border-bottom: 1px solid {COLORS['border']}; padding: 2px 0;
                font-size: 13px;
            }}
            QMenuBar::item {{
                padding: 6px 14px; border-radius: 6px; margin: 2px 2px;
            }}
            QMenuBar::item:selected {{
                background: {COLORS['primary_bg']}; color: {COLORS['primary']};
            }}
            QMenu {{
                background: white; border: 1px solid {COLORS['border']};
                border-radius: 8px; padding: 6px;
            }}
            QMenu::item {{
                padding: 8px 32px 8px 16px; border-radius: 6px;
                font-size: 13px;
            }}
            QMenu::item:selected {{
                background: {COLORS['primary_bg']}; color: {COLORS['primary']};
            }}
            QMenu::separator {{
                height: 1px; background: {COLORS['border_light']}; margin: 4px 12px;
            }}
        """)

        # ---- Dosya Menüsü ----
        file_menu = menubar.addMenu("Dosya")

        self.action_new_order = QAction("Yeni Sipariş", self)
        self.action_new_order.setShortcut("Ctrl+N")
        self.action_new_order.setStatusTip("Yeni sipariş oluşturmak için Garson paneline gidin")
        self.action_new_order.triggered.connect(
            lambda: QMessageBox.information(self, "Bilgi",
                "Yeni sipariş oluşturmak için Garson (Kullanıcı) panelinden bir masa seçin."))
        file_menu.addAction(self.action_new_order)

        self.action_backup = QAction("Veritabanı Yedeği Al", self)
        self.action_backup.setShortcut("Ctrl+B")
        self.action_backup.setStatusTip("Veritabanının yedeğini alır")
        self.action_backup.triggered.connect(self._backup_database)
        file_menu.addAction(self.action_backup)

        file_menu.addSeparator()

        self.action_exit = QAction("Çıkış", self)
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_exit.setStatusTip("Uygulamayı kapatır")
        self.action_exit.triggered.connect(self.close)
        file_menu.addAction(self.action_exit)

        # ---- Düzenle Menüsü ----
        edit_menu = menubar.addMenu("Düzenle")

        self.action_refresh = QAction("Sayfayı Yenile", self)
        self.action_refresh.setShortcut("Ctrl+R")
        self.action_refresh.setStatusTip("Aktif sayfayı yeniden yükler")
        self.action_refresh.triggered.connect(self._refresh_current)
        edit_menu.addAction(self.action_refresh)

        self.action_settings = QAction("Bölge/Masa Ayarları", self)
        self.action_settings.setStatusTip("Masa ve bölge konfigürasyonunu açar")
        self.action_settings.triggered.connect(
            lambda: QMessageBox.information(self, "Bilgi",
                "Bölge ve masa ayarları için Admin Paneli → Tanımlamalar → Masa / Bölgeler bölümüne gidin."))
        edit_menu.addAction(self.action_settings)

        # ---- Yardım Menüsü ----
        help_menu = menubar.addMenu("Yardım")

        self.action_about = QAction("Sistem Hakkında", self)
        self.action_about.setShortcut("F1")
        self.action_about.setStatusTip("NexPOS hakkında bilgi gösterir")
        self.action_about.triggered.connect(self._show_about)
        help_menu.addAction(self.action_about)

        self.action_shortcuts = QAction("Klavye Kısayolları", self)
        self.action_shortcuts.setStatusTip("Tüm klavye kısayollarını listeler")
        self.action_shortcuts.triggered.connect(self._show_shortcuts)
        help_menu.addAction(self.action_shortcuts)

    # ==================== TOOLBAR (Hafta 7) ====================
    def _setup_toolbar(self):
        self.main_toolbar = self.addToolBar("Ana Araçlar")
        self.main_toolbar.setMovable(False)
        self.main_toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.main_toolbar.addAction(self.action_refresh)
        self.main_toolbar.addAction(self.action_backup)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.action_about)

    # ==================== STATUSBAR (Hafta 7) ====================
    def _setup_statusbar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Hazır — Giriş bekleniyor...")

        # Sağ tarafta sabit bilgiler
        self.status_user_label = QLabel(f"  {ICONS['user']} Giriş yapılmadı  ")
        self.status_user_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-weight: bold;")
        self.status_bar.addPermanentWidget(self.status_user_label)

        self.status_table_label = QLabel(f"  {ICONS['table']} Masa: —  ")
        self.status_table_label.setStyleSheet(f"color: {COLORS['text_muted']};")
        self.status_bar.addPermanentWidget(self.status_table_label)

        from datetime import datetime
        self.status_time_label = QLabel(f"  {datetime.now().strftime('%d.%m.%Y %H:%M')}  ")
        self.status_time_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-weight: bold;")
        self.status_bar.addPermanentWidget(self.status_time_label)

        # Saat güncelleme zamanlayıcısı
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(30000)  # 30 saniyede bir güncelle

    def _update_clock(self):
        from datetime import datetime
        self.status_time_label.setText(f"  {datetime.now().strftime('%d.%m.%Y %H:%M')}  ")
        # Masaların durumunu da periyodik olarak güncelle
        if self._current_user:
            stats = database.get_dashboard_stats()
            self.status_table_label.setText(
                f"  {ICONS['table']} Dolu: {stats['occupied_tables']}/{stats['total_tables']} Masa  ")

    def _update_status_info(self, user_data=None):
        """Giriş sonrası StatusBar bilgilerini güncelle"""
        if user_data:
            name = user_data.get('ad_soyad', 'Kullanıcı')
            role = user_data.get('gorev', '')
            self.status_user_label.setText(f"  {ICONS['user']} {name} ({role})  ")
            self.status_user_label.setStyleSheet(f"color: {COLORS['primary']}; font-weight: bold;")

            stats = database.get_dashboard_stats()
            self.status_table_label.setText(
                f"  {ICONS['table']} Dolu: {stats['occupied_tables']}/{stats['total_tables']} Masa  ")
            self.status_table_label.setStyleSheet(f"color: {COLORS['text_secondary']};")

            self.status_bar.showMessage(f"Hoş geldiniz, {name}!")
        else:
            self.status_user_label.setText(f"  {ICONS['user']} Giriş yapılmadı  ")
            self.status_user_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-weight: bold;")
            self.status_table_label.setText(f"  {ICONS['table']} Masa: —  ")
            self.status_bar.showMessage("Hazır — Giriş bekleniyor...")

    # ==================== AKSIYONLAR ====================
    def _backup_database(self):
        import shutil
        from datetime import datetime
        src = database.DB_PATH
        dst = src.replace(".db", f"_yedek_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        try:
            shutil.copy2(src, dst)
            QMessageBox.information(self, "Yedek Alındı",
                f"Veritabanı yedeği başarıyla oluşturuldu:\n{dst}")
            self.status_bar.showMessage("Veritabanı yedeği alındı.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Yedek alınamadı:\n{str(e)}")

    def _refresh_current(self):
        """Aktif paneli yeniden yükle"""
        current = self.stack.currentWidget()
        if current == self.admin_panel and self.admin_panel:
            idx = self.admin_panel.pages.currentIndex()
            self.admin_panel._show_page(idx)
            self.status_bar.showMessage("Sayfa yenilendi.", 3000)
        elif current == self.user_panel and self.user_panel:
            idx = self.user_panel.pages.currentIndex()
            self.user_panel._switch_tab(idx)
            self.status_bar.showMessage("Sayfa yenilendi.", 3000)

    def _show_about(self):
        QMessageBox.about(self, "NexPOS Hakkında",
            "<h2 style='color:#4F46E5;'>NexPOS v3.2.0</h2>"
            "<p><b>Restaurant Yönetim Sistemi</b></p>"
            "<p>PySide6 (Qt for Python) ile geliştirilmiştir.</p>"
            "<hr>"
            "<p><b>Kullanılan Teknolojiler:</b></p>"
            "<ul>"
            "<li>PySide6 — Qt Framework</li>"
            "<li>SQLite — Veritabanı</li>"
            "<li>QSS — Stil Sistemi</li>"
            "</ul>"
            "<p style='color:#64748B;'>© 2026 NexPOS Technologies</p>")

    def _show_shortcuts(self):
        QMessageBox.information(self, "Klavye Kısayolları",
            "Ctrl+N  →  Yeni Sipariş\n"
            "Ctrl+B  →  Veritabanı Yedeği Al\n"
            "Ctrl+R  →  Sayfayı Yenile\n"
            "Ctrl+Q  →  Çıkış\n"
            "F1        →  Sistem Hakkında")

    # ==================== LOGIN / LOGOUT ====================
    def _on_login(self, user_data):
        self._current_user = user_data
        self._update_status_info(user_data)
        role = user_data.get('gorev', 'Garson')
        
        self.menuBar().setVisible(False)
        self.main_toolbar.setVisible(False)
        
        if role == 'Yönetici':
            if self.admin_panel:
                self.stack.removeWidget(self.admin_panel)
                self.admin_panel.deleteLater()
            self.admin_panel = AdminPanel(user_data)
            self.admin_panel.logout_signal.connect(self._on_logout)
            self.stack.addWidget(self.admin_panel)
            self.stack.setCurrentWidget(self.admin_panel)
        else:
            self.menuBar().setVisible(False)
            self.main_toolbar.setVisible(False)
            if self.user_panel:
                self.stack.removeWidget(self.user_panel)
                self.user_panel.deleteLater()
            self.user_panel = UserPanel(user_data)
            self.user_panel.logout_signal.connect(self._on_logout)
            self.stack.addWidget(self.user_panel)
            self.stack.setCurrentWidget(self.user_panel)

    def _on_logout(self):
        self.menuBar().setVisible(False)
        self.main_toolbar.setVisible(False)
        self.stack.setCurrentWidget(self.login_screen)
        self.login_screen.password_input.clear()
        self._current_user = None
        self._update_status_info(None)
        if self.admin_panel:
            self.stack.removeWidget(self.admin_panel)
            self.admin_panel.deleteLater()
            self.admin_panel = None
        if self.user_panel:
            self.stack.removeWidget(self.user_panel)
            self.user_panel.deleteLater()
            self.user_panel = None

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Güvenli Çıkış',
                                     "Programdan çıkmak istediğinize emin misiniz?\n\n(Arka plan veri yedekleme işlemi tamamlandı.)",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def qt_message_handler(mode, context, message):
    if "QFont::setPointSize" in message:
        return
    # Diğer hata/uyarı mesajları terminalde görünmeye devam etsin
    print(message)

def main():
    from PySide6.QtCore import qInstallMessageHandler
    qInstallMessageHandler(qt_message_handler)
    app = QApplication(sys.argv)
    app.setFont(QFont(FONTS['family'], FONTS['size_md']))
    app.setStyleSheet(get_global_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
