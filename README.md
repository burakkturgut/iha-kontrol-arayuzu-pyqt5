# İstikbal İHA Yer Kontrol Arayüzü

Bu proje, sabit kanatlı otonom İnsansız Hava Araçları (İHA) için geliştirilen bir **Yer Kontrol Arayüzü** yazılımıdır. PyQt5 tabanlı bu sistem; canlı video akışı, harita üzerinden İHA takibi, görev modu yönetimi, telemetri izleme, QR kod okuma ve kullanıcı giriş kontrolü gibi fonksiyonları tek bir arayüzde birleştirir. Sistem, yarışma formatındaki görev senaryolarına uygun şekilde modüler ve ölçeklenebilir olarak tasarlanmıştır.

---

##  Temel Özellikler

-  **Kullanıcı Girişi**: `users.json` üzerinden tanımlı kullanıcılar ile doğrulama
-  **Gerçek Zamanlı Kamera Akışı**: OpenCV ile sistem kamerasından canlı görüntü
-  **Harita Tabanlı Takip**: Folium ve Leaflet.js destekli interaktif konum haritası
-  **Pixhawk Telemetri Entegrasyonu**: MAVLink protokolü ile GPS, hız, irtifa ve batarya verileri
-  **Görev Modları**: Otonom kalkış, uçuş, iniş, kilitlenme, kamikaze görev kontrolü
-  **QR Kod Okuma**: Pyzbar ile kameradan gerçek zamanlı QR tespiti ve görev verisi gönderimi
-  **Sunucu Entegrasyonu**: Flask tabanlı test sunucusuna bağlantı ve veri iletimi
-  **Test API Sunucusu**: `test_sunucu.py` ile yerel sunucu simülasyonu

---

##  Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|----------|----------|
| Python 3 | Ana yazılım dili |
| PyQt5    | Arayüz geliştirme |
| OpenCV   | Kamera akışı ve görüntü işleme |
| Folium   | Harita görselleştirme |
| Pyzbar   | QR kod tespiti |
| Pymavlink| Pixhawk üzerinden MAVLink haberleşme |
| Flask    | Sunucu simülasyonu için mikro framework |
| JSON     | Kullanıcı yönetimi ve veri iletişimi |


---

##  Proje Yapısı

```bash
iha-yer-kontrol-arayuzu/
├── main.py                  # Ana kontrol arayüzü
├── LoginWindow.py          # Giriş ekranı
├── sunucu.py               # Sunucu haberleşme fonksiyonları
├── test_sunucu.py          # Flask tabanlı test sunucu
├── users.json              # Kullanıcı listesi
├── harita_demo_bandirma.html # Başlangıç harita HTML’i
├── istikbal.png            # Giriş ekranı logosu
├── arkaplan.jpg            # Arayüz için arka plan (isteğe bağlı)
├── requirements.txt        # Python kütüphaneleri listesi
└── README.md               # Bu doküman
```

---

##  Kurulum ve Çalıştırma Adımları

###  Gerekli Kütüphaneleri Kurun

```bash
pip install -r requirements.txt
```

> Bu komut, projede kullanılan tüm bağımlılıkları (pyqt5, opencv-python, folium, flask, pyzbar, pymavlink) kurar. Ortamın sağlıklı şekilde hazırlanması için bu ilk adımdır.

Alternatif olarak:

```bash
pip install pyqt5 opencv-python folium pyzbar pymavlink flask
```

> Paketleri manuel kurmak istersen bu komutu tercih edebilirsin.

---

###  Uygulamayı Başlat

```bash
python main.py
```

> Giriş ekranı (LoginWindow) açılır. Doğrulama sonrası ana kontrol arayüzü başlatılır.

---

###  Test Sunucusunu Başlat (Opsiyonel)

```bash
python test_sunucu.py
```

> QR kodu okuma ve görev verisini test etmek için Flask tabanlı örnek bir API sunucusudur.

---

##  Kullanıcı Bilgileri (varsayılan)

Kullanıcı doğrulama işlemi `users.json` üzerinden yapılır:

```json
[
  { "username": "Burak", "password": "1234" },
  { "username": "Aydın", "password": "1234" },
  { "username": "Eren", "password": "1234" },
  { "username": "Alim", "password": "1234" }
]
```

---

##  Teknik Açıklamalar

- **Pixhawk Telemetri**: MAVLink protokolü ile COM port üzerinden Pixhawk ile bağlantı kurulur. Konum, hız, irtifa, batarya ve uçuş modu verileri alınır ve GUI üzerinden kullanıcıya sunulur.
- **QR Kod Okuma**: Kamera görüntüsü üzerinden `pyzbar.decode()` ile QR kod tespiti yapılır. Başarılı okuma durumunda veri Flask sunucusuna HTTP POST ile gönderilir.
- **Harita Güncelleme**: İHA’nın anlık konumu değiştikçe yeni HTML harita dosyası oluşturulur ve arayüzde gösterilir.
- **Görev Butonları**: Otonom görevler (kalkış, iniş, kamikaze) kullanıcı girişine bağlı olarak aktif hale gelir. Her işlem log olarak ekrana yazılır.

---

##  Geliştirici

**Burak Turgut**  
Bandırma Onyedi Eylül Üniversitesi  
Bilgisayar Mühendisliği  
E-posta: burak.turgut.dev@gmail.com  
GitHub: [github.com/burakkturgut](https://github.com/burakkturgut)
LinkedIn: [linkedin.com/in/burakkturgut](https://www.linkedin.com/in/burakkturgut)

---

##  Akademik Not

Bu projede yer alan tüm yazılım bileşenleri ve kodlar, bireysel geliştirme sürecine dayanmaktadır. Herhangi bir bölümünün izinsiz olarak kullanılması, kaynak gösterilmeksizin paylaşılması veya başka bir projede doğrudan kopyalanması etik dışıdır ve akademik dürüstlüğe aykırıdır.

Projeyi kullanmak, referans vermek veya katkıda bulunmak isterseniz lütfen benimle iletişime geçiniz. Her türlü bilimsel iş birliğine açığım.

İletişim: burak.turgut.dev@gmail.com  

---

#  İstikbal UAV Ground Control Interface

This project is a **Ground Control Interface** software developed for fixed-wing autonomous Unmanned Aerial Vehicles (UAVs). Built with PyQt5, the system integrates live video streaming, map-based UAV tracking, mission mode management, telemetry monitoring, QR code scanning, and user login control into a single interface. The system is modular and scalable, designed to be compatible with competition-style mission scenarios.

---

##  Key Features

-  **User Login**: Authentication via `users.json` defined users
-  **Real-Time Camera Feed**: Live video from system camera using OpenCV
-  **Map-Based Tracking**: Interactive location map supported by Folium and Leaflet.js
-  **Pixhawk Telemetry Integration**: Data such as GPS, speed, altitude, battery status via MAVLink
-  **Mission Modes**: Autonomous takeoff, flight, landing, lock-on, and kamikaze control
-  **QR Code Scanning**: Real-time QR code detection and task data submission using Pyzbar
-  **Server Integration**: Connection and data transmission with Flask-based test server
-  **Test API Server**: Local server simulation with `test_sunucu.py`

---

##  Technologies Used

| Technology | Description |
|------------|-------------|
| Python 3   | Core programming language |
| PyQt5      | GUI development |
| OpenCV     | Camera and image processing |
| Folium     | Map generation |
| Pyzbar     | QR code detection |
| Pymavlink  | MAVLink communication with Pixhawk |
| Flask      | Lightweight test server framework |
| JSON       | User and data management format |

---

##  Project Structure

```bash
iha-yer-kontrol-arayuzu/
├── main.py                  # Main control interface
├── LoginWindow.py          # User login screen
├── sunucu.py               # Server communication functions
├── test_sunucu.py          # Flask-based test server
├── users.json              # User credentials
├── harita_demo_bandirma.html # Initial map HTML
├── istikbal.png            # Login screen logo
├── arkaplan.jpg            # Optional background image
├── requirements.txt        # Required Python packages
└── README.md               # This documentation file
```

---

##  Setup and Execution Steps

###  Install Required Packages

```bash
pip install -r requirements.txt
```

> This command installs all dependencies (pyqt5, opencv-python, folium, flask, pyzbar, pymavlink) listed in the project. It is the first essential step for a clean environment.

Alternatively:

```bash
pip install pyqt5 opencv-python folium pyzbar pymavlink flask
```

> Use this command to manually install packages one by one if preferred.

---

###  Launch the Application

```bash
python main.py
```

> The login screen (LoginWindow) will appear. Upon successful authentication, the main control interface launches.

---

###  Start the Test Server (Optional)

```bash
python test_sunucu.py
```

> A sample Flask-based API server used to simulate QR scanning and mission data submission.

---

##  Default User Credentials

Users are defined in `users.json`:

```json
[
  { "username": "Burak", "password": "1234" },
  { "username": "Aydın", "password": "1234" },
  { "username": "Eren", "password": "1234" },
  { "username": "Alim", "password": "1234" }
]
```

---

##  Technical Explanations

- **Pixhawk Telemetry**: Communicates with Pixhawk via COM port using MAVLink. Retrieves GPS, speed, altitude, battery, and flight mode data and displays it on the GUI.
- **QR Code Detection**: Real-time QR scanning via `pyzbar.decode()` from the camera feed. On success, data is submitted via HTTP POST to the Flask server.
- **Map Update**: As the UAV’s location updates, a new HTML map is generated and reloaded into the GUI.
- **Mission Buttons**: Autonomous missions (takeoff, landing, kamikaze) are activated through user input. Logs are displayed on screen in real-time.

---

##  Developer

**Burak Turgut**  
Bandırma Onyedi Eylül University  
Department of Computer Engineering  
Email: burak.turgut.dev@gmail.com  
GitHub: [github.com/burakkturgut](https://github.com/burakkturgut) \n LinkedIn: [linkedin.com/in/burakkturgut](https://www.linkedin.com/in/burakkturgut)"

---

##  Academic Notice

All software components and codes in this project are the result of individual development. Using any part of it without permission, sharing it without citation, or directly copying it into another project is considered unethical and violates academic integrity.

🎓 If you wish to use this project, cite it, or collaborate scientifically, please contact me.

📧 Contact: burak.turgut.dev@gmail.com
