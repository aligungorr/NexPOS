"""
NexPOS - Veritabanı Katmanı
"""
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexpos.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_database():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_soyad TEXT NOT NULL, email TEXT, telefon TEXT,
        sifre TEXT NOT NULL, gorev TEXT NOT NULL DEFAULT 'Garson',
        aktif INTEGER DEFAULT 1, son_giris TEXT, son_cikis TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL, sira INTEGER DEFAULT 0)""")

    c.execute("""CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL, region_id INTEGER NOT NULL, durum TEXT DEFAULT 'bos',
        garson_id INTEGER,
        FOREIGN KEY (region_id) REFERENCES regions(id),
        FOREIGN KEY (garson_id) REFERENCES users(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL, renk TEXT DEFAULT '#6C5CE7', sira INTEGER DEFAULT 0)""")

    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL, fiyat REAL NOT NULL DEFAULT 0,
        kategori_id INTEGER, birim TEXT DEFAULT 'Tam', aktif INTEGER DEFAULT 1,
        FOREIGN KEY (kategori_id) REFERENCES categories(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        masa_id INTEGER, garson_id INTEGER, durum TEXT DEFAULT 'hazirlaniyor',
        toplam_tutar REAL DEFAULT 0, tarih TEXT, notlar TEXT,
        FOREIGN KEY (masa_id) REFERENCES tables(id),
        FOREIGN KEY (garson_id) REFERENCES users(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
        adet INTEGER DEFAULT 1, birim_fiyat REAL, toplam REAL, notlar TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        masraf_tipi TEXT, tutar REAL, odeme_tipi TEXT DEFAULT 'Nakit',
        masraf_detayi TEXT, kullanici_id INTEGER, masraf_tarihi TEXT, eklenme_tarihi TEXT,
        FOREIGN KEY (kullanici_id) REFERENCES users(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS waste (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER, zayi_nedeni TEXT, adet INTEGER DEFAULT 1,
        maliyet_tutari REAL DEFAULT 0, sorumlu_id INTEGER,
        zayi_tarihi TEXT, eklenme_tarihi TEXT,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (sorumlu_id) REFERENCES users(id))""")

    conn.commit()

    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        _create_sample_data(conn)
    conn.close()


def _create_sample_data(conn):
    c = conn.cursor()

    users = [
        ("Deniz Yılmaz", "admin@nexpos.com", "5321234567", hash_password("admin123"), "Yönetici"),
        ("Cem Akar", "cem@nexpos.com", "5359876543", hash_password("garson123"), "Garson"),
        ("Elif Demir", "elif@nexpos.com", "5447654321", hash_password("garson123"), "Garson"),
    ]
    c.executemany("INSERT INTO users (ad_soyad,email,telefon,sifre,gorev) VALUES (?,?,?,?,?)", users)

    c.execute("INSERT INTO regions (ad,sira) VALUES ('Salon',1)")
    salon_id = c.lastrowid
    c.execute("INSERT INTO regions (ad,sira) VALUES ('Teras',2)")
    teras_id = c.lastrowid
    c.execute("INSERT INTO regions (ad,sira) VALUES ('Bahçe',3)")
    bahce_id = c.lastrowid

    for i in range(1, 9):
        c.execute("INSERT INTO tables (ad,region_id) VALUES (?,?)", (f"Masa {i}", salon_id))
    for i in range(9, 17):
        c.execute("INSERT INTO tables (ad,region_id) VALUES (?,?)", (f"Masa {i}", teras_id))
    for i in range(17, 25):
        c.execute("INSERT INTO tables (ad,region_id) VALUES (?,?)", (f"Masa {i}", bahce_id))

    cats = [
        ("Sıcak Kahveler", "#8D6E63"), ("Soğuk Kahveler", "#795548"),
        ("Sıcak İçecekler", "#FF7043"), ("Soğuk İçecekler", "#42A5F5"),
        ("Tatlı ve Pastalar", "#EC407A"), ("Kahvaltılar", "#FFA726"),
        ("Atıştırmalıklar", "#66BB6A"), ("Ana Yemekler", "#EF5350"),
        ("Salatalar", "#26A69A"), ("Tostlar & Sandviçler", "#AB47BC"),
    ]
    cat_ids = []
    for cat in cats:
        c.execute("INSERT INTO categories (ad,renk) VALUES (?,?)", cat)
        cat_ids.append(c.lastrowid)

    products = [
        ("Türk Kahvesi", 60, cat_ids[0]), ("Latte", 85, cat_ids[0]),
        ("Americano", 75, cat_ids[0]), ("Cappuccino", 80, cat_ids[0]),
        ("Mocha", 90, cat_ids[0]),
        ("Ice Latte", 90, cat_ids[1]), ("Cold Brew", 95, cat_ids[1]),
        ("Frappe", 85, cat_ids[1]),
        ("Çay", 30, cat_ids[2]), ("Bitki Çayı", 45, cat_ids[2]),
        ("Sahlep", 65, cat_ids[2]), ("Sıcak Çikolata", 70, cat_ids[2]),
        ("Limonata", 70, cat_ids[3]), ("Meyveli Soda", 60, cat_ids[3]),
        ("Smoothie", 90, cat_ids[3]),
        ("San Sebastian", 130, cat_ids[4]), ("Tiramisu", 110, cat_ids[4]),
        ("Brownie", 95, cat_ids[4]), ("Cheesecake", 120, cat_ids[4]),
        ("Serpme Kahvaltı", 450, cat_ids[5]), ("Sahanda Yumurta", 120, cat_ids[5]),
        ("Menemen", 110, cat_ids[5]),
        ("Patates Kızartması", 85, cat_ids[6]), ("Soğan Halkası", 95, cat_ids[6]),
        ("Izgara Tavuk", 195, cat_ids[7]), ("Köfte Tabağı", 185, cat_ids[7]),
        ("Sezar Salata", 140, cat_ids[8]), ("Akdeniz Salata", 130, cat_ids[8]),
        ("Tost", 90, cat_ids[9]), ("Kulüp Sandviç", 140, cat_ids[9]),
    ]
    for p in products:
        c.execute("INSERT INTO products (ad,fiyat,kategori_id) VALUES (?,?,?)", p)

    now = datetime.now()
    orders = [
        (2, 2, "hazirlaniyor", 255.00, (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")),
        (5, 3, "hazirlaniyor", 450.00, (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")),
        (11, 2, "bekliyor", 170.00, (now - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")),
        (18, 3, "hazirlaniyor", 320.00, (now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M")),
    ]
    for o in orders:
        c.execute("INSERT INTO orders (masa_id,garson_id,durum,toplam_tutar,tarih) VALUES (?,?,?,?,?)", o)
        c.execute("UPDATE tables SET durum='dolu', garson_id=? WHERE id=?", (o[1], o[0]))

    conn.commit()


# ---- CRUD ----

def authenticate_user(email_or_phone, password):
    conn = get_connection()
    hashed = hash_password(password)
    user = conn.execute(
        "SELECT * FROM users WHERE (email=? OR telefon=?) AND sifre=? AND aktif=1",
        (email_or_phone, email_or_phone, hashed)).fetchone()
    if user:
        conn.execute("UPDATE users SET son_giris=? WHERE id=?",
                      (datetime.now().strftime("%d.%m.%Y %H:%M"), user['id']))
        conn.commit()
    conn.close()
    return dict(user) if user else None


def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_user(ad_soyad, email, telefon, sifre, gorev):
    conn = get_connection()
    conn.execute("INSERT INTO users (ad_soyad,email,telefon,sifre,gorev) VALUES (?,?,?,?,?)",
                 (ad_soyad, email, telefon, hash_password(sifre), gorev))
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


def get_all_regions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM regions ORDER BY sira").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_region(ad):
    conn = get_connection()
    mx = conn.execute("SELECT COALESCE(MAX(sira),0) FROM regions").fetchone()[0]
    conn.execute("INSERT INTO regions (ad,sira) VALUES (?,?)", (ad, mx + 1))
    conn.commit()
    conn.close()


def delete_region(region_id):
    conn = get_connection()
    conn.execute("DELETE FROM tables WHERE region_id=?", (region_id,))
    conn.execute("DELETE FROM regions WHERE id=?", (region_id,))
    conn.commit()
    conn.close()


def get_tables_by_region(region_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT t.*, u.ad_soyad as garson_adi,
               o.toplam_tutar, o.tarih as siparis_tarihi
        FROM tables t
        LEFT JOIN users u ON t.garson_id = u.id
        LEFT JOIN orders o ON o.masa_id = t.id AND o.durum IN ('hazirlaniyor','bekliyor')
        WHERE t.region_id = ? ORDER BY t.id
    """, (region_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_table(ad, region_id):
    conn = get_connection()
    conn.execute("INSERT INTO tables (ad,region_id) VALUES (?,?)", (ad, region_id))
    conn.commit()
    conn.close()


def delete_table(table_id):
    conn = get_connection()
    conn.execute("DELETE FROM tables WHERE id=?", (table_id,))
    conn.commit()
    conn.close()


def get_all_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY sira,id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_category(ad, renk="#6C5CE7"):
    conn = get_connection()
    mx = conn.execute("SELECT COALESCE(MAX(sira),0) FROM categories").fetchone()[0]
    conn.execute("INSERT INTO categories (ad,renk,sira) VALUES (?,?,?)", (ad, renk, mx + 1))
    conn.commit()
    conn.close()


def delete_category(cat_id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE kategori_id=?", (cat_id,))
    conn.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    conn.close()


def get_products_by_category(kategori_id=None):
    conn = get_connection()
    if kategori_id:
        rows = conn.execute("SELECT * FROM products WHERE kategori_id=? AND aktif=1 ORDER BY id",
                            (kategori_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM products WHERE aktif=1 ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_product(ad, fiyat, kategori_id, birim="Tam"):
    conn = get_connection()
    conn.execute("INSERT INTO products (ad,fiyat,kategori_id,birim) VALUES (?,?,?,?)",
                 (ad, fiyat, kategori_id, birim))
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    conn.execute("UPDATE products SET aktif=0 WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def get_orders(durum=None):
    conn = get_connection()
    q = """SELECT o.*, t.ad as masa_adi, u.ad_soyad as garson_adi
           FROM orders o LEFT JOIN tables t ON o.masa_id=t.id
           LEFT JOIN users u ON o.garson_id=u.id"""
    if durum:
        q += " WHERE o.durum=?"
        rows = conn.execute(q + " ORDER BY o.tarih DESC", (durum,)).fetchall()
    else:
        rows = conn.execute(q + " ORDER BY o.tarih DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_order_items(order_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT oi.*, p.ad as urun_adi
        FROM order_items oi LEFT JOIN products p ON oi.product_id=p.id
        WHERE oi.order_id=? ORDER BY oi.id
    """, (order_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_order(masa_id, garson_id, items):
    conn = get_connection()
    c = conn.cursor()
    toplam = 0
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO orders (masa_id,garson_id,durum,tarih) VALUES (?,?,?,?)",
              (masa_id, garson_id, "hazirlaniyor", tarih))
    order_id = c.lastrowid
    for product_id, adet in items:
        product = c.execute("SELECT fiyat FROM products WHERE id=?", (product_id,)).fetchone()
        if product:
            bf = product[0]
            t = bf * adet
            toplam += t
            c.execute("INSERT INTO order_items (order_id,product_id,adet,birim_fiyat,toplam) VALUES (?,?,?,?,?)",
                      (order_id, product_id, adet, bf, t))
    c.execute("UPDATE orders SET toplam_tutar=? WHERE id=?", (toplam, order_id))
    c.execute("UPDATE tables SET durum='dolu', garson_id=? WHERE id=?", (garson_id, masa_id))
    conn.commit()
    conn.close()
    return order_id


def update_order_status(order_id, new_status):
    conn = get_connection()
    conn.execute("UPDATE orders SET durum=? WHERE id=?", (new_status, order_id))
    if new_status in ('tamamlandi', 'iptal'):
        order = conn.execute("SELECT masa_id FROM orders WHERE id=?", (order_id,)).fetchone()
        if order:
            active = conn.execute(
                "SELECT COUNT(*) FROM orders WHERE masa_id=? AND durum NOT IN ('tamamlandi','iptal')",
                (order['masa_id'],)).fetchone()[0]
            if active == 0:
                conn.execute("UPDATE tables SET durum='bos', garson_id=NULL WHERE id=?", (order['masa_id'],))
    conn.commit()
    conn.close()


def get_expenses(start_date=None, end_date=None):
    conn = get_connection()
    q = "SELECT e.*, u.ad_soyad as kullanici_adi FROM expenses e LEFT JOIN users u ON e.kullanici_id=u.id"
    params = []
    if start_date and end_date:
        q += " WHERE e.masraf_tarihi BETWEEN ? AND ?"
        params = [start_date, end_date]
    rows = conn.execute(q + " ORDER BY e.masraf_tarihi DESC", params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_expense(masraf_tipi, tutar, odeme_tipi, masraf_detayi, kullanici_id, masraf_tarihi):
    conn = get_connection()
    conn.execute("""INSERT INTO expenses (masraf_tipi,tutar,odeme_tipi,masraf_detayi,kullanici_id,masraf_tarihi,eklenme_tarihi)
        VALUES (?,?,?,?,?,?,?)""",
        (masraf_tipi, tutar, odeme_tipi, masraf_detayi, kullanici_id, masraf_tarihi,
         datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()


def get_waste(start_date=None, end_date=None):
    conn = get_connection()
    q = """SELECT w.*, p.ad as urun_adi, u.ad_soyad as sorumlu_adi
           FROM waste w LEFT JOIN products p ON w.product_id=p.id
           LEFT JOIN users u ON w.sorumlu_id=u.id"""
    params = []
    if start_date and end_date:
        q += " WHERE w.zayi_tarihi BETWEEN ? AND ?"
        params = [start_date, end_date]
    rows = conn.execute(q + " ORDER BY w.zayi_tarihi DESC", params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_waste(product_id, zayi_nedeni, adet, maliyet, sorumlu_id, zayi_tarihi):
    conn = get_connection()
    conn.execute("""INSERT INTO waste (product_id,zayi_nedeni,adet,maliyet_tutari,sorumlu_id,zayi_tarihi,eklenme_tarihi)
        VALUES (?,?,?,?,?,?,?)""",
        (product_id, zayi_nedeni, adet, maliyet, sorumlu_id, zayi_tarihi,
         datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()


def get_dashboard_stats():
    conn = get_connection()
    today = datetime.now().strftime("%Y-%m-%d")
    ts = conn.execute("SELECT COALESCE(SUM(toplam_tutar),0) FROM orders WHERE date(tarih)=? AND durum='tamamlandi'", (today,)).fetchone()[0]
    gc = conn.execute("SELECT COUNT(DISTINCT masa_id) FROM orders WHERE date(tarih)=?", (today,)).fetchone()[0]
    oo = conn.execute("SELECT COALESCE(SUM(toplam_tutar),0) FROM orders WHERE durum IN ('hazirlaniyor','bekliyor')").fetchone()[0]
    te = conn.execute("SELECT COALESCE(SUM(tutar),0) FROM expenses WHERE date(masraf_tarihi)=?", (today,)).fetchone()[0]
    tt = conn.execute("SELECT COUNT(*) FROM tables").fetchone()[0]
    oc = conn.execute("SELECT COUNT(*) FROM tables WHERE durum='dolu'").fetchone()[0]
    conn.close()
    return {'total_sales': ts, 'guest_count': gc, 'open_orders': oo,
            'total_expense': te, 'total_tables': tt, 'occupied_tables': oc}


def get_expense_summary(start_date=None, end_date=None):
    """Masraf tipine göre gruplu özet"""
    conn = get_connection()
    q = """SELECT masraf_tipi, COUNT(*) as islem_sayisi, SUM(tutar) as toplam_tutar,
           odeme_tipi FROM expenses"""
    params = []
    if start_date and end_date:
        q += " WHERE masraf_tarihi BETWEEN ? AND ?"
        params = [start_date, end_date]
    q += " GROUP BY masraf_tipi ORDER BY toplam_tutar DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_expense_payment_summary(start_date=None, end_date=None):
    """Ödeme tipine göre gruplu özet"""
    conn = get_connection()
    q = "SELECT odeme_tipi, SUM(tutar) as toplam FROM expenses"
    params = []
    if start_date and end_date:
        q += " WHERE masraf_tarihi BETWEEN ? AND ?"
        params = [start_date, end_date]
    q += " GROUP BY odeme_tipi"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return {r['odeme_tipi']: r['toplam'] for r in rows}


def get_waste_summary(start_date=None, end_date=None):
    """Ürüne göre gruplu zayi özeti"""
    conn = get_connection()
    q = """SELECT p.ad as urun_adi, SUM(w.adet) as toplam_adet,
           SUM(w.maliyet_tutari) as toplam_maliyet
           FROM waste w LEFT JOIN products p ON w.product_id=p.id"""
    params = []
    if start_date and end_date:
        q += " WHERE w.zayi_tarihi BETWEEN ? AND ?"
        params = [start_date, end_date]
    q += " GROUP BY w.product_id ORDER BY toplam_maliyet DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_waste(waste_id):
    conn = get_connection()
    conn.execute("DELETE FROM waste WHERE id=?", (waste_id,))
    conn.commit()
    conn.close()

