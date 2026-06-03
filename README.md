<div align="center">

# NexPOS — Kafe & Restoran Yönetim Sistemi

**Python · PySide6 · SQLite · OOP**

Kafe ve restoran işletmelerinin masa takibi, sipariş yönetimi, finansal raporlama ve personel yetkilendirme süreçlerini tek bir merkezden yöneten masaüstü otomasyon yazılımı.

</div>

---

## İçindekiler

- [Özellikler](#özellikler)
- [Teknolojiler](#teknolojiler)
- [Dosya Yapısı](#dosya-yapısı)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Demo Hesaplar](#demo-hesaplar)
- [Proje Ekibi](#proje-ekibi)

---

## Özellikler

### Garson Paneli
- Salon, Teras, Bahçe gibi bölgelere ayrılmış masa görünümü — dolu/boş durumu renk kodlu kartlarla anlık takip
- Ürün arama ve kategori filtreleme ile hızlı sipariş oluşturma
- Sipariş notu ekleme ("az şekerli", "allerji var" vb.)
- İskonto uygulama (yüzde bazlı, anlık net tutar önizlemesi)
- Masa transfer — aktif siparişi başka bir masaya taşıma
- Sipariş panosu: Mutfakta / Hazır aşamalarını gerçek zamanlı takip
- Vardiya özeti — o güne ait tamamlanan sipariş sayısı ve toplam ciro
- Nakit / Kredi Kartı ödeme alma ve masa otomatik kapatma

### Yönetici Paneli
- Dashboard: Son 30 günlük satış, açık siparişler, gider ve masa doluluk özeti
- Masa ve bölge yönetimi — yeni bölge/masa ekleme, mevcut masaları düzenleme
- Menü yönetimi — kategori ve ürün ekleme/düzenleme/silme (soft-delete, geçmiş siparişler korunur)
- Kullanıcı yönetimi — personel ekleme, rol atama, aktif/pasif durumu
- Yetkilendirme matrisi — Garson, Kurye, Kasa, Müdür, Yönetici rolleri için işlem bazlı izin yönetimi
- Gider / Masraf takibi — tarih filtreli listeleme ve özet
- Zayi yönetimi — bozulan veya hatalı üretilen ürünlerin stoktan düşülmesi
- İstatistikler — gerçekleşen satış, ortalama adisyon, iskonto raporu, en popüler 5 ürün
- CSV dışa aktarma
- Ctrl+B ile tek tıkla veritabanı yedekleme

### Teknik
- Rol tabanlı erişim kontrolü (RBAC) — her kullanıcı yalnızca kendi panelini görür
- SHA-256 şifre doğrulama
- QTimer ile 30 saniyelik otomatik masa doluluk güncelleme
- Global crash handler — beklenmedik hatalar `crash_log.txt`'e yazılır
- Tüm veritabanı işlemleri Foreign Key kısıtlı, cascade-safe

---

## Teknolojiler

| Bileşen | Teknoloji |
|---|---|
| Programlama Dili | Python 3.10+ |
| GUI Framework | PySide6 (Qt for Python) |
| Veritabanı | SQLite 3 |
| Mimari | Nesne Yönelimli Programlama (OOP) |
| Stil | QSS (Qt Style Sheets) |

---

## Dosya Yapısı

```
nexpos/
├── main.py            # Uygulama giriş noktası — QMainWindow, login → panel yönlendirme
├── database.py        # Tüm veritabanı işlemleri (CRUD, kimlik doğrulama, raporlama)
├── login_screen.py    # Giriş ekranı ve kullanıcı doğrulama
├── admin_panel.py     # Yönetici paneli (dashboard, ürün, masa, kullanıcı, raporlar)
├── user_panel.py      # Garson paneli (masa seçimi, sipariş, pano, ödeme)
├── widgets.py         # Özel UI bileşenleri (TableCard, OrderCard, StatCard, ToastNotification)
├── styles.py          # Merkezi renk paleti, font ve QSS stil tanımları
├── requirements.txt   # Bağımlılık listesi
├── nexpos.db          # SQLite veritabanı — demo verilerle birlikte
├── Brew_Flow_NexPOS_Uygulama_Kullanim_Kilavuzu.docx   # Kullanım kılavuzu
└── NexPOS_EXE/        # Windows için derlenmiş hazır uygulama
    ├── NexPOS.exe     # Çalıştırılabilir uygulama (Python gerektirmez)
    └── nexpos.db      # Uygulamayla birlikte gelen veritabanı
```

> `nexpos.db` repoda demo verilerle hazır gelir. Silinirse, uygulama ilk çalıştırmada veritabanını ve demo verileri otomatik olarak yeniden oluşturur.

---

## Kurulum

Uygulamayı iki şekilde çalıştırabilirsiniz.

### Seçenek 1 — Hazır uygulama (Windows .exe)

Python kurulumu **gerektirmez**. `NexPOS_EXE` klasöründeki **NexPOS.exe** dosyasına çift tıklayın.

Uygulama, yanındaki `nexpos.db` veritabanıyla birlikte gelir; bu nedenle mevcut veriler korunur. Veritabanı dosyası silinse veya bulunamasa bile, uygulama ilk açılışta veritabanını ve demo verileri otomatik olarak oluşturur.

### Seçenek 2 — Kaynaktan çalıştırma (Python)

**Gereksinimler:** Python **3.10** veya üzeri ([indir](https://www.python.org/downloads/)) ve pip

**1. Repoyu klonlayın**

```bash
git clone https://github.com/aligungorr/nexpos.git
cd nexpos
```

**2. Bağımlılıkları yükleyin**

```bash
pip install -r requirements.txt
```

Yalnızca `PySide6` kurulması yeterlidir. Diğer modüller (`sqlite3`, `hashlib`, `json`, `datetime` vb.) Python standart kütüphanesinde yer almaktadır.

**3. Uygulamayı başlatın**

```bash
python main.py
```

Bu yöntemde de `nexpos.db` veritabanı mevcutsa kullanılır; silinmişse veya hiç yoksa ilk çalıştırmada otomatik olarak oluşturulur. Herhangi bir ek yapılandırmaya gerek yoktur.

---

## Kullanım

Uygulama başlatıldığında giriş ekranı açılır. Kullanıcı adı (e-posta veya telefon) ve şifre girilerek sisteme giriş yapılır. Giriş başarılı olduğunda kullanıcı rolüne göre otomatik yönlendirme gerçekleşir:

- **Yönetici** girişi → Admin Paneli
- **Garson** girişi → Garson Paneli

### Temel İş Akışı (Garson)

```
Giriş → Bölgeler → Masa Seç → Sipariş Oluştur → Mutfağa Gönder → Ödeme Al → Masa Kapandı
```

### Temel İş Akışı (Yönetici)

```
Giriş → Dashboard → Tanımlamalar (Masa / Menü) → Raporlar → Kullanıcı Yönetimi
```

---

## Demo Hesaplar

Veritabanı oluşturulduğunda aşağıdaki test hesapları hazır gelir:

| Rol | E-posta | Şifre |
|---|---|---|
| Yönetici | admin@nexpos.com | admin123 |
| Garson | cem@nexpos.com | garson123 |
| Garson | elif@nexpos.com | garson123 |

> Üretim ortamında bu şifrelerin değiştirilmesi önerilir.

---

## Proje Ekibi

| İsim | Öğrenci No |
|---|---|
| Ali Güngör | 23010708021 |
| Emirhan Yusuf Arslan | 22640708002 |

---

<div align="center">

Bu proje **Görsel Programlama II** dersi kapsamında akademik amaçla geliştirilmiştir.

**Bartın Üniversitesi · 2025–2026**

</div>
