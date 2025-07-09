from flask import Flask, request, jsonify

app = Flask(__name__)

# Takım kimlik bilgileri (örnek)
TAKIM_KULLANICI = "takimkadi"
TAKIM_SIFRE = "takimsifresi"
TAKIM_NUMARASI = 42

@app.route("/api/giris", methods=["POST"])
def giris():
    veri = request.get_json()

    if veri is None:
        return "Geçersiz JSON", 400

    kadi = veri.get("kadi")
    sifre = veri.get("sifre")

    if kadi == TAKIM_KULLANICI and sifre == TAKIM_SIFRE:
        return jsonify({"takim_numarasi": TAKIM_NUMARASI}), 200
    else:
        return "Kullanıcı adı veya şifre hatalı", 400

@app.route("/api/sunucusaati", methods=["GET"])
def sunucu_saati():
    from datetime import datetime
    now = datetime.utcnow()

    return jsonify({
        "gun": now.day,
        "saat": now.hour,
        "dakika": now.minute,
        "saniye": now.second,
        "milisaniye": int(now.microsecond / 1000)
    })

@app.route("/api/kamikaze_bilgisi", methods=["POST"])
def kamikaze_bilgisi():
    veri = request.get_json()

    if not veri:
        return "Geçersiz veri", 400

    bas = veri.get("kamikazeBaslangicZamani")
    bit = veri.get("kamikazeBitisZamani")
    qr = veri.get("qrMetni")

    if not bas or not bit or not qr:
        return "Eksik bilgi", 400

    print("🚀 Kamikaze Bilgisi Alındı:")
    print(f"Başlangıç: {bas}, Bitiş: {bit}, QR: {qr}")
    return "Kamikaze verisi alındı", 200


if __name__ == "__main__":
    app.run(host="127.0.0.25", port=5000, debug=True)
