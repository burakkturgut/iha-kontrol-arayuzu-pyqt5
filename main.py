import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QGroupBox, QRadioButton, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import cv2
from sunucu import sunucuya_baglan, sunucu_saati_al, kamikaze_verisi_gonder

from pymavlink import mavutil



def harita_olustur(html_dosya_yolu, merkez, kendi_iha):
    import folium

    harita = folium.Map(location=merkez, zoom_start=17)

    folium.Marker(
        location=kendi_iha,
        popup="Bizim İHA",
        icon=folium.Icon(color='blue')
    ).add_to(harita)

    harita.save(html_dosya_yolu)



class IHAKontrolArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İSTİKBAL İHA Yer Kontrol Arayüzü")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # ÜST: Kamera ve Harita
        ust_layout = QHBoxLayout()
        self.kamera_label = QLabel("KAMERA GÖRÜNTÜSÜ")
        self.kamera_label.setAlignment(Qt.AlignCenter)
        self.kamera_label.setFixedSize(700, 400)
        self.kamera_label.setStyleSheet("background-color: #444; border: 2px solid #555; font-size: 18px;")
        
        self.harita_view = QWebEngineView()
        harita_path = os.path.abspath("harita_demo_bandirma.html")  # doğru dosya
        harita_olustur(harita_path, merkez=(40.0, 27.0), kendi_iha=(40.0, 27.0))
        self.harita_view.load(QUrl.fromLocalFile(harita_path))
        self.harita_view.setFixedSize(800, 400)

        ust_layout.addWidget(self.kamera_label)
        ust_layout.addWidget(self.harita_view)

        # ALT: Bilgiler ve Butonlar
        alt_layout = QGridLayout()

        def grup_kutu(baslik, icerikler):
            grup = QGroupBox(baslik)
            grup.setObjectName(baslik)
            layout = QVBoxLayout()
            self.label_refs = getattr(self, "label_refs", {})  # Eğer yoksa oluştur
            for eleman in icerikler:
                label = QLabel(eleman)
                layout.addWidget(label)
                if "QR Durumu" in eleman:
                    self.qr_label = label  # Erişilebilir hale getiriyoruz
            grup.setLayout(layout)
            return grup


        self.telemetry_box = grup_kutu("Telemetri", ["GPS: --", "Hız: --", "İrtifa: --", "Batarya: --", "Mod: --"])
        kilit_qr = grup_kutu("Kilitlenme / QR", ["Kilitlenme:--", "QR Durumu:--"])
        sunucu = QGroupBox("Sunucu")
        sunucu_layout = QVBoxLayout()

        self.sunucu_durum_label = QLabel("Durum: --")
        sunucu_layout.addWidget(self.sunucu_durum_label)

        sunucu_baglan_btn = QPushButton("Sunucuya Bağlan")
        sunucu_baglan_btn.clicked.connect(self.baglan_sunucu)
        sunucu_layout.addWidget(sunucu_baglan_btn)

        sunucu.setLayout(sunucu_layout)


        gorev_modu = QGroupBox("Uçuş Modu")
        gorev_layout = QVBoxLayout()

        self.mod_secim = QComboBox()
        self.mod_secim.addItems(["AUTO", "MANUAL"])
        gorev_layout.addWidget(self.mod_secim)

        mod_degistir_buton = QPushButton("Modu Değiştir")
        mod_degistir_buton.clicked.connect(self.mod_degistir)
        gorev_layout.addWidget(mod_degistir_buton)

        gorev_modu.setLayout(gorev_layout)


        butonlar = QGroupBox("Kontroller")
        buton_layout = QVBoxLayout()
        sistemi_baslat_butonu = QPushButton("Sistemi Başlat")
        sistemi_baslat_butonu.clicked.connect(self.start_camera)
        buton_layout.addWidget(sistemi_baslat_butonu)

        pixhawk_baglan_buton = QPushButton("Pixhawk Telemetri Başlat")
        pixhawk_baglan_buton.clicked.connect(self.basla_telemetri)
        buton_layout.addWidget(pixhawk_baglan_buton)

        self.gorev_butonlari = ["Otonom Kalkış", "Otonom Uçuş", "Otonom İniş", " HSS Başlat", "Sistem Durdur"]
        for yazi in self.gorev_butonlari:
            btn = QPushButton(yazi)
            btn.clicked.connect(self.gorev_buton_kontrol)
            buton_layout.addWidget(btn)
        butonlar.setLayout(buton_layout)

        # LOG PANELİ (küçük, sol alt)
        log_panel = QGroupBox("İşlem Logları")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setFixedHeight(150)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #1e1e1e;")
        log_layout.addWidget(self.log_text)
        log_panel.setLayout(log_layout)
        log_panel.setFixedHeight(220)

        # GÖREV MODU SEÇİMİ (sağ alt)
        gorev_panel = QGroupBox("Görev Modu")
        gorev_panel_layout = QVBoxLayout()
        self.kilit_btn = QPushButton("Kilitlenme Görevi")
        self.kamikaze_btn = QPushButton("Kamikaze Görevi")
        self.kamikaze_btn.clicked.connect(self.kamikaze_qr_baslat)

        

        self.kilit_btn.setCheckable(True)
        self.kamikaze_btn.setCheckable(True)
        self.kilit_btn.clicked.connect(self.kilitlenme_gorevi_placeholder)

        # Aynı anda sadece biri seçilebilsin diye
        from PyQt5.QtWidgets import QButtonGroup
        self.gorev_button_group = QButtonGroup()
        self.gorev_button_group.addButton(self.kilit_btn)
        self.gorev_button_group.addButton(self.kamikaze_btn)
       

        gorev_panel_layout.addWidget(self.kilit_btn)
        gorev_panel_layout.addWidget(self.kamikaze_btn)
        

        gorev_panel.setLayout(gorev_panel_layout)
        gorev_panel.setFixedHeight(220)


        # Alt alt: Log + Görev yan yana
        log_gorev_hbox = QHBoxLayout()
        log_gorev_hbox.addWidget(log_panel, stretch=1)
        log_gorev_hbox.addWidget(gorev_panel, stretch=1)


        alt_layout.addWidget(self.telemetry_box, 0, 0)
        alt_layout.addWidget(kilit_qr, 0, 1)
        alt_layout.addWidget(sunucu, 0, 2)
        alt_layout.addWidget(gorev_modu, 0, 3)
        alt_layout.addWidget(butonlar, 0, 4)
        alt_layout.addLayout(log_gorev_hbox, 1, 0, 1, 5)

        ana_layout.addLayout(ust_layout)
        ana_layout.addLayout(alt_layout)
        self.setLayout(ana_layout)

        # İşlem loguna sahte veriler
        
        #self.log_text.append("📡 Telemetri gönderildi.")
        #self.log_text.append("🎯 Görev: Kilitlenme aktif.")

        #    Kilitlenme görevini seçili hale getir
        self.kilit_btn.setChecked(True)

        #    Diğer kutulara sahte veriler yaz


        self.qr_okuma_aktif = False
        self.sistem_baslatildi = False


        # Kamera ve harita alanlarına örnek yazı
        #self.kamera_label.setText("CANLI GÖRÜNTÜ AKTARILIYOR")

    def gorev_buton_kontrol(self):
        if not self.sistem_baslatildi:
            self.log_text.append("⚠️ Lütfen önce sistemi başlatın.")
            return

        buton = self.sender()
        self.log_text.append(f"🔘 {buton.text()} komutu gönderildi.")


    def start_camera(self):
        self.capture = cv2.VideoCapture(0)  # 0 = dahili kamera (gerekirse 1 yap)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera_frame)
        self.timer.start(30)
        self.sistem_baslatildi = True


    def update_camera_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.kamera_label.setPixmap(QPixmap.fromImage(qimg).scaled(
                self.kamera_label.width(), self.kamera_label.height(), aspectRatioMode=1))
            
            # QR kod okuma kısmı
            if self.qr_okuma_aktif and not self.qr_kod_okundu:
                from pyzbar.pyzbar import decode
                decoded_objs = decode(frame)
                for obj in decoded_objs:
                    qr_verisi = obj.data.decode('utf-8')
                    self.qr_kod_okundu = True
                    self.log_text.append(f"📦 QR kodu okundu: {qr_verisi}")
                    self.qr_label.setText("📷 QR kod okuma başarılı ✅")
                    self.qr_label.setStyleSheet("color: lightgreen;")
                    try:
                        bas = sunucu_saati_al()
                        bit = sunucu_saati_al()  # İleride 10 saniye sonra alabilirsin
                        qr_verisi = qr_verisi.strip()
                        kamikaze_verisi_gonder(bas, bit, qr_verisi)
                        self.log_text.append("📤 Kamikaze verisi sunucuya gönderildi.")
                    except Exception as e:
                        self.log_text.append(f"❌ Kamikaze gönderim hatası: {str(e)}")
                    break

    def baglan_sunucu(self):
        if not self.sistem_baslatildi:
            self.log_text.append("⚠️ Sunucuya bağlanmak için önce sistemi başlatın.")
            return
        
        kadi = "takimkadi"
        sifre = "takimsifresi"

        try:
            takim_no = sunucuya_baglan(kadi, sifre)
            self.sunucu_durum_label.setText(f"Durum: ✅ Bağlandı | Takım No: {takim_no}")
            self.log_text.append(f"🔌 Sunucuya başarıyla bağlanıldı. Takım No: {takim_no}")
            self.takim_numarasi = takim_no

            # ⏰ Sunucu saatini al
            saat = sunucu_saati_al()
            self.log_text.append(f"🕒 Sunucu Saati: {saat['saat']:02}:{saat['dakika']:02}:{saat['saniye']:02}.{saat['milisaniye']:03}")

        except Exception as e:
            self.sunucu_durum_label.setText("Durum: ❌ Bağlantı Hatası")
            self.log_text.append(str(e))

    def kilitlenme_gorevi_placeholder(self):
        if not self.sistem_baslatildi:
            self.log_text.append("⚠️ Lütfen önce sistemi başlatın.")
            return
        self.log_text.append("ℹ️ Kilitlenme görevi henüz aktif değil. Geliştirme aşamasında.")

    def kamikaze_qr_baslat(self):
        if not self.sistem_baslatildi:
            self.log_text.append("⚠️ Lütfen önce sistemi başlatın.")
            return

        self.qr_kod_okundu = False
        self.qr_okuma_aktif = True
        self.log_text.append("🎯 Kamikaze görevi başlatıldı. QR kod okunuyor...")

    def basla_telemetri(self):
        try:
            # Pixhawk bağlantısı başlatılıyor
            self.master = mavutil.mavlink_connection('COM7', baud=57600)  # COM portunu kendi bulduğunla değiştir
            self.master.wait_heartbeat(timeout=10)
            self.log_text.append("✅ Pixhawk ile bağlantı kuruldu.")
            
            # 1 saniyede bir verileri güncelle
            self.telemetri_timer = QTimer()
            self.telemetri_timer.timeout.connect(self.guncelle_telemetri)
            self.telemetri_timer.start(1000)
        except Exception as e:
            self.log_text.append(f"❌ Pixhawk bağlantı hatası: {str(e)}")

    def guncelle_telemetri(self):
        try:
            msg = self.master.recv_match(type=['GLOBAL_POSITION_INT', 'SYS_STATUS', 'HEARTBEAT'], blocking=False)
            if not msg:
                return
            
            for i in range(self.telemetry_box.layout().count()):
                label = self.telemetry_box.layout().itemAt(i).widget()
                text = label.text()
                
                if text.startswith("GPS"):
                    gps_text = f"GPS: {msg.lat/1e7:.6f}, {msg.lon/1e7:.6f}" if msg.get_type() == "GLOBAL_POSITION_INT" else label.text()
                    label.setText(gps_text)

                elif text.startswith("İrtifa"):
                    irtifa = msg.alt / 1000 if msg.get_type() == "GLOBAL_POSITION_INT" else None
                    if irtifa:
                        label.setText(f"İrtifa: {irtifa:.1f} m")

                elif text.startswith("Hız"):
                    hiz = ((msg.vx ** 2 + msg.vy ** 2 + msg.vz ** 2) ** 0.5) / 100 if msg.get_type() == "GLOBAL_POSITION_INT" else None
                    if hiz:
                        label.setText(f"Hız: {hiz:.1f} m/s")

                elif text.startswith("Batarya"):
                    batarya = msg.battery_remaining if msg.get_type() == "SYS_STATUS" else None
                    if batarya is not None:
                        label.setText(f"Batarya: {batarya}%")

                elif text.startswith("Mod"):
                    if msg.get_type() == "HEARTBEAT":
                        mode_id = msg.custom_mode
                        mode_mapping = self.master.mode_mapping()
                        mode_name = next((k for k, v in mode_mapping.items() if v == mode_id), "Bilinmiyor")
                        label.setText(f"Mod: {mode_name}")
                        
                # Harita konumu güncelle
            if msg.get_type() == "GLOBAL_POSITION_INT":
                yeni_lat = msg.lat / 1e7
                yeni_lon = msg.lon / 1e7

                if not hasattr(self, 'son_konum') or self.son_konum != (yeni_lat, yeni_lon):
                    self.son_konum = (yeni_lat, yeni_lon)

                    harita_olustur(
                        html_dosya_yolu="harita_demo_bandirma.html",
                        merkez=self.son_konum,
                        kendi_iha=self.son_konum
                    )
                    self.harita_view.reload()
                    
        except Exception as e:
            self.log_text.append(f"⚠️ Telemetri okuma hatası: {str(e)}")

    def mod_degistir(self):
        if not hasattr(self, 'master'):
            self.log_text.append("⚠️ Pixhawk bağlantısı yapılmadı.")
            return

        try:
            secilen_mod = self.mod_secim.currentText()
            mode_mapping = self.master.mode_mapping()
            mode_id = mode_mapping.get(secilen_mod)

            if mode_id is None:
                self.log_text.append(f"❌ Seçilen mod desteklenmiyor: {secilen_mod}")
                return

            self.master.set_mode(mode_id)
            self.log_text.append(f"🔄 Uçuş modu değiştirildi: {secilen_mod}")
        except Exception as e:
            self.log_text.append(f"❌ Mod değiştirme hatası: {str(e)}")


#if __name__ == "__main__":
    #app = QApplication(sys.argv)
    #pencere = IHAKontrolArayuzu()
    #pencere.show()
    #sys.exit(app.exec_())

if __name__ == "__main__":
    from LoginWindow import LoginWindow
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

