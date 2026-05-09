"""
NexPOS - Premium Stil Sistemi
Koyu sidebar, gradient vurgular, glassmorphism, profesyonel POS tasarımı
"""

COLORS = {
    # Ana renkler
    'primary': '#4F46E5',        # Indigo
    'primary_dark': '#3730A3',
    'primary_light': '#818CF8',
    'primary_bg': '#EEF2FF',

    'accent': '#F59E0B',          # Amber
    'accent_dark': '#D97706',
    'accent_light': '#FCD34D',

    # Sidebar - Koyu tema
    'sidebar_bg': '#0F172A',      # Slate 900
    'sidebar_hover': '#1E293B',   # Slate 800
    'sidebar_active': '#4F46E5',
    'sidebar_text': '#94A3B8',    # Slate 400
    'sidebar_text_active': '#FFFFFF',
    'sidebar_border': '#1E293B',
    'sidebar_header': '#1E293B',

    # Arka planlar
    'bg_main': '#F1F5F9',         # Slate 100
    'bg_white': '#FFFFFF',
    'bg_card': '#FFFFFF',
    'bg_hover': '#F8FAFC',
    'bg_input': '#F8FAFC',
    'bg_success': '#ECFDF5',
    'bg_warning': '#FFFBEB',
    'bg_danger': '#FEF2F2',

    # Metin
    'text_dark': '#0F172A',
    'text_primary': '#1E293B',
    'text_secondary': '#64748B',
    'text_muted': '#94A3B8',
    'text_white': '#FFFFFF',

    # Border
    'border': '#E2E8F0',
    'border_light': '#F1F5F9',
    'border_focus': '#4F46E5',

    # Kart renkleri - StatCard
    'card_blue': '#3B82F6',
    'card_blue_bg': '#EFF6FF',
    'card_green': '#10B981',
    'card_green_bg': '#ECFDF5',
    'card_orange': '#F59E0B',
    'card_orange_bg': '#FFFBEB',
    'card_red': '#EF4444',
    'card_red_bg': '#FEF2F2',
    'card_purple': '#8B5CF6',
    'card_purple_bg': '#F5F3FF',
    'card_pink': '#EC4899',
    'card_pink_bg': '#FDF2F8',
    'card_teal': '#14B8A6',
    'card_teal_bg': '#F0FDFA',
    'card_indigo': '#6366F1',
    'card_indigo_bg': '#EEF2FF',
    'card_amber': '#F59E0B',
    'card_amber_bg': '#FFFBEB',

    # Masa durumları
    'table_empty': '#FFFFFF',
    'table_empty_border': '#E2E8F0',
    'table_occupied': '#FEF2F2',
    'table_occupied_border': '#F87171',
    'table_reserved': '#FFFBEB',
    'table_reserved_border': '#FBBF24',

    # Durum renkleri
    'success': '#10B981',
    'success_dark': '#059669',
    'warning': '#F59E0B',
    'warning_dark': '#D97706',
    'danger': '#EF4444',
    'danger_dark': '#DC2626',
    'info': '#3B82F6',
    'info_dark': '#2563EB',
}

FONTS = {
    'family': 'Segoe UI',
    'size_xs': 10,
    'size_sm': 11,
    'size_md': 13,
    'size_lg': 15,
    'size_xl': 20,
    'size_xxl': 26,
    'size_hero': 34,
    'size_display': 42,
}

# Unicode ikonlar - Windows uyumlu
ICONS = {
    'home': '\u2302',        # ⌂
    'settings': '\u2699',    # ⚙
    'user': '\u2603',        # Placeholder
    'chart': '\u2261',       # ≡
    'table': '\u25A3',       # ▣
    'menu_food': '\u2630',   # ☰
    'money': '\u20BA',       # ₺
    'arrow_right': '\u25B6', # ▶
    'arrow_down': '\u25BC',  # ▼
    'check': '\u2713',       # ✓
    'cross': '\u2717',       # ✗
    'plus': '+',
    'minus': '\u2212',       # −
    'dot': '\u2022',         # •
    'star': '\u2605',        # ★
    'circle': '\u25CF',      # ●
    'square': '\u25A0',      # ■
    'diamond': '\u25C6',     # ◆
    'triangle': '\u25B2',    # ▲
    'edit': '\u270E',        # ✎
    'trash': '\u2716',       # ✖
    'search': '\u2315',      # ⌕
    'bell': '\u2407',        #
    'lock': '\u2616',        # ☖
    'logout': '\u2192',      # →
    'refresh': '\u21BB',     # ↻
    'print': '\u2399',       # ⎙
    'save': '\u2193',        # ↓
    'expand': '\u25B8',      # ▸
    'collapse': '\u25BE',    # ▾
}


def get_global_stylesheet():
    return f"""
    * {{
        font-family: '{FONTS['family']}';
        outline: none;
    }}

    QMainWindow {{
        background-color: {COLORS['bg_main']};
    }}

    /* ===== BUTONLAR ===== */
    QPushButton#primaryBtn {{
        background: {COLORS['primary']};
        color: white;
        border: none;
        font-weight: bold;
        font-size: 14px;
        padding: 12px 32px;
        border-radius: 10px;
        min-height: 40px;
    }}
    QPushButton#primaryBtn:hover {{
        background: {COLORS['primary_dark']};
    }}
    QPushButton#primaryBtn:pressed {{
        background: #312E81;
    }}

    QPushButton#successBtn {{
        background: {COLORS['success']};
        color: white;
        border: none;
        font-weight: bold;
        font-size: 14px;
        padding: 12px 32px;
        border-radius: 10px;
        min-height: 40px;
    }}
    QPushButton#successBtn:hover {{
        background: {COLORS['success_dark']};
    }}

    QPushButton#dangerBtn {{
        background: {COLORS['danger']};
        color: white;
        border: none;
        font-weight: bold;
        font-size: 14px;
        padding: 12px 32px;
        border-radius: 10px;
        min-height: 40px;
    }}
    QPushButton#dangerBtn:hover {{
        background: {COLORS['danger_dark']};
    }}

    QPushButton#outlineBtn {{
        background: transparent;
        color: {COLORS['primary']};
        border: 2px solid {COLORS['primary']};
        font-weight: bold;
        font-size: 13px;
        padding: 10px 24px;
        border-radius: 10px;
        min-height: 36px;
    }}
    QPushButton#outlineBtn:hover {{
        background: {COLORS['primary_bg']};
    }}

    QPushButton#ghostBtn {{
        background: transparent;
        color: {COLORS['text_secondary']};
        border: none;
        font-size: 13px;
        padding: 8px 16px;
        border-radius: 8px;
    }}
    QPushButton#ghostBtn:hover {{
        background: {COLORS['bg_hover']};
        color: {COLORS['primary']};
    }}

    /* ===== INPUT ===== */
    QLineEdit {{
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 13px;
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_dark']};
        selection-background-color: {COLORS['primary_light']};
    }}
    QLineEdit:focus {{
        border-color: {COLORS['primary']};
        background-color: white;
    }}

    /* ===== TABLE ===== */
    QTableWidget {{
        background-color: white;
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        gridline-color: {COLORS['border_light']};
        selection-background-color: {COLORS['primary_bg']};
        font-size: 13px;
        alternate-background-color: #E2E8F0;
    }}
    QTableWidget::item {{
        padding: 10px 12px;
        border-bottom: 1px solid {COLORS['border_light']};
    }}
    QTableWidget::item:selected {{
        background-color: {COLORS['primary_bg']};
        color: {COLORS['primary']};
    }}
    QTableWidget QHeaderView::section {{
        background-color: {COLORS['sidebar_bg']};
        border: none;
        padding: 14px 12px;
        font-weight: 700;
        color: {COLORS['text_white']};
        font-size: 12px;
        text-transform: uppercase;
    }}

    /* ===== COMBOBOX ===== */
    QComboBox {{
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 8px 14px;
        background-color: {COLORS['bg_input']};
        font-size: 13px;
        min-height: 20px;
        color: {COLORS['text_dark']};
    }}
    QComboBox:focus {{
        border-color: {COLORS['primary']};
        background: white;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox QAbstractItemView {{
        background: white;
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        selection-background-color: {COLORS['primary_bg']};
        selection-color: {COLORS['primary']};
        padding: 4px;
    }}

    /* ===== DATE/SPIN ===== */
    QDateEdit {{
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 8px 14px;
        background-color: {COLORS['bg_input']};
        font-size: 13px;
    }}
    QDateEdit:focus {{
        border-color: {COLORS['primary']};
    }}

    QSpinBox, QDoubleSpinBox {{
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 8px 14px;
        background-color: {COLORS['bg_input']};
        font-size: 13px;
        color: {COLORS['text_dark']};
    }}
    QSpinBox:focus, QDoubleSpinBox:focus {{
        border-color: {COLORS['primary']};
        background-color: white;
    }}
    QSpinBox::up-button, QDoubleSpinBox::up-button {{
        background: transparent;
        border-left: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        margin-top: 2px; margin-right: 2px; border-top-right-radius: 8px;
    }}
    QSpinBox::down-button, QDoubleSpinBox::down-button {{
        background: transparent;
        border-left: 1px solid {COLORS['border']};
        margin-bottom: 2px; margin-right: 2px; border-bottom-right-radius: 8px;
    }}
    QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
    QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
        background: {COLORS['bg_hover']};
    }}

    /* ===== SCROLL ===== */
    QScrollArea {{
        border: none;
        background: transparent;
    }}
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        border-radius: 4px;
        margin: 4px 0;
    }}
    QScrollBar::handle:vertical {{
        background: {COLORS['text_muted']};
        border-radius: 4px;
        min-height: 40px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLORS['text_secondary']};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background: {COLORS['text_muted']};
        border-radius: 4px;
        min-width: 40px;
    }}

    /* ===== DIALOG ===== */
    QDialog {{
        background-color: white;
        border-radius: 16px;
    }}

    /* ===== MESSAGEBOX ===== */
    QMessageBox {{
        background-color: white;
    }}
    QMessageBox QLabel {{
        font-size: 14px;
        min-width: 350px;
        min-height: 80px;
        padding: 16px;
        color: {COLORS['text_dark']};
    }}
    QMessageBox QPushButton {{
        min-width: 120px;
        min-height: 40px;
        font-size: 13px;
        border-radius: 10px;
        padding: 10px 28px;
        background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
        color: white;
        border: none;
        font-weight: bold;
    }}
    QMessageBox QPushButton:hover {{
        background: {COLORS['primary_dark']};
    }}

    /* ===== CHECKBOX ===== */
    QCheckBox {{
        font-size: 13px;
        color: {COLORS['text_secondary']};
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {COLORS['border']};
        border-radius: 6px;
        background: white;
    }}
    QCheckBox::indicator:checked {{
        background: {COLORS['primary']};
        border-color: {COLORS['primary']};
    }}

    /* ===== TOOLTIP ===== */
    QToolTip {{
        background: {COLORS['sidebar_bg']};
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 12px;
    }}

    /* ===== TOOLBAR ===== */
    QToolBar {{
        background: {COLORS['bg_white']};
        border-bottom: 1px solid {COLORS['border']};
        padding: 4px 8px;
        spacing: 8px;
    }}
    QToolBar QToolButton {{
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: bold;
        color: {COLORS['text_secondary']};
    }}
    QToolBar QToolButton:hover {{
        background: {COLORS['primary_bg']};
        color: {COLORS['primary']};
        border-color: {COLORS['border']};
    }}

    /* ===== STATUSBAR ===== */
    QStatusBar {{
        background: {COLORS['bg_white']};
        border-top: 1px solid {COLORS['border']};
        color: {COLORS['text_secondary']};
        font-size: 12px;
        padding: 4px 16px;
    }}
    QStatusBar QLabel {{
        color: {COLORS['text_secondary']};
        font-size: 12px;
        padding: 0 8px;
    }}

    /* ===== PROGRESSBAR ===== */
    QProgressBar {{
        border: none;
        border-radius: 6px;
        background: {COLORS['border_light']};
        text-align: center;
        font-size: 11px;
        color: {COLORS['text_secondary']};
        min-height: 12px;
        max-height: 12px;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
            stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_light']});
        border-radius: 6px;
    }}

    /* ===== CALENDAR & DATE EDIT ===== */
    QDateEdit {{
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 8px 14px;
        background-color: {COLORS['bg_input']};
        font-size: 13px;
        color: {COLORS['text_dark']};
    }}
    QDateEdit:focus {{
        border-color: {COLORS['primary']};
        background-color: white;
    }}
    QDateEdit::drop-down {{
        border: none;
        width: 30px;
    }}
    QDateEdit::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['text_secondary']};
        margin-right: 10px;
    }}
    QCalendarWidget QWidget {{
        alternate-background-color: {COLORS['bg_hover']};
        background-color: white;
    }}
    QCalendarWidget QAbstractItemView:enabled {{
        font-size: 13px;
        color: {COLORS['text_dark']};
        background-color: white;
        selection-background-color: {COLORS['primary']};
        selection-color: white;
    }}
    QCalendarWidget QToolButton {{
        color: white;
        background-color: {COLORS['primary']};
        border-radius: 4px;
        font-weight: bold;
    }}
    QCalendarWidget QMenu {{
        background-color: white;
    }}
    QCalendarWidget QSpinBox {{
        background-color: white;
        color: {COLORS['text_dark']};
    }}
    """
