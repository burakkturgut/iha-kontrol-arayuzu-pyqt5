# sunucu.py
import requests

def sunucuya_baglan(kadi, sifre):
    try:
        response = requests.post("http://127.0.0.25:5000/api/giris", json={
            "kadi": kadi,
            "sifre": sifre
        })
        if response.status_code == 200:
            return response.json().get("takim_numarasi")
        elif response.status_code == 400:
            raise Exception("❌ Kullanıcı adı veya şifre hatalı.")
        elif response.status_code == 401:
            raise Exception("❌ Oturum açılmadan erişim denemesi.")
        else:
            raise Exception(f"❌ Sunucu hatası: {response.status_code}")
    except Exception as e:
        raise Exception(f"❌ Hata: {str(e)}")

def sunucu_saati_al():
    try:
        response = requests.get("http://127.0.0.25:5000/api/sunucusaati")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Sunucu saati alınamadı: {response.status_code}")
    except Exception as e:
        raise Exception(f"Sunucu saati hatası: {str(e)}")

def kamikaze_verisi_gonder(baslangic, bitis, qr_metni):
    url = "http://127.0.0.25:5000/api/kamikaze_bilgisi"
    payload = {
        "kamikazeBaslangicZamani": baslangic,
        "kamikazeBitisZamani": bitis,
        "qrMetni": qr_metni
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Kamikaze verisi gönderilemedi: {response.status_code}")
    except Exception as e:
        raise Exception(f"Hata: {str(e)}")
