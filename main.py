import os
from flask import Flask, request
import requests
import math

app = Flask(__name__)

TOKEN = "8922760802:AAFncprMJK_pCHpkPdnhIpeQE0uBej71vYQ"
CHAT_ID = "-1003215449646"

def tablo_olustur(yon, g1, g2, stop, tp1, tp2, tp3):
    # 1. Dinamik Kaldıraç Hesaplama
    # Mantık: Stop mesafesi arttıkça kaldıraç düşer. 
    # Örn: %8 stop için -> 32 / 8 = 4x kaldıraç.
    stop_mesafesi = abs((stop - g1) / g1) * 100
    kaldirac = math.floor(32 / stop_mesafesi) 
    if kaldirac < 1: kaldirac = 1
    if kaldirac > 20: kaldirac = 20 # Maksimum 20x sınır koyduk

    def hesapla(seviye_fiyat):
        spot_degisim = ((seviye_fiyat - g1) / g1) * 100
        if yon.lower() == "short": spot_degisim *= -1
        kaldiracli = spot_degisim * kaldirac
        return f"{spot_degisim:+.1f}%", f"{kaldiracli:+.1f}%"

    s_stop, k_stop = hesapla(stop)
    s_tp1, k_tp1 = hesapla(tp1)
    s_tp2, k_tp2 = hesapla(tp2)
    s_tp3, k_tp3 = hesapla(tp3)

    emoji_yon = "🔴 SHORT" if yon.lower() == "short" else "🟢 LONG"

    tablo = (
        f"📊 **ONDER ACADEMY SETUP ({emoji_yon})**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡️ **Kaldıraç:** {kaldirac}x (Otomatik Ayarlandı)\n"
        f"🎯 **Giriş Bölgesi:** {g1} - {g2}\n"
        f"⚠️ *OB içinde parçalı alım yapınız.*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"```\n"
        f"Seviye      Fiyat      Spot     {kaldirac:>2}x P/L\n"
        f"----------  ---------  -------  --------\n"
        f"Stop Loss   {stop:<9}  {s_stop:<7}  {k_stop}\n"
        f"Giriş 1     {g1:<9}  0.0%     %0.0\n"
        f"TP 1        {tp1:<9}  {s_tp1:<7}  {k_tp1}\n"
        f"TP 2        {tp2:<9}  {s_tp2:<7}  {k_tp2}\n"
        f"TP 3        {tp3:<9}  {s_tp3:<7}  {k_tp3}\n"
        f"```\n"
        f"🛡 **RİSK:** Cüzdanın **1/50**'si (%2) ile girin.\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    return tablo

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        mesaj = tablo_olustur(
            data.get("yon"),
            float(data.get("g1")),
            float(data.get("g2")),
            float(data.get("stop")),
            float(data.get("tp1")),
            float(data.get("tp2")),
            float(data.get("tp3"))
        )
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"})
        return {"status": "success"}, 200
    except:
        return {"status": "error"}, 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
