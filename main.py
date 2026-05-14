import os
from flask import Flask, request
import requests

app = Flask(__name__)

# --- ONDER ACADEMY BILGILERI ---
TOKEN = "8922760802:AAFncprMJK_pCHpkPdnhIpeQE0uBej71vYQ"
CHAT_ID = "-1003215449646"

@app.route('/')
def home():
    return "Onder Academy Botu Canli!", 200

def tema_olustur(sinyal_adi):
    s = sinyal_adi.lower()
    if "bullish" in s and "ob" in s: return "🟢 **BULLISH ORDER BLOCK**", "📦"
    elif "bearish" in s and "ob" in s: return "🔴 **BEARISH ORDER BLOCK**", "📦"
    elif "bos" in s: return "⚡️ **MARKET STRUCTURE BREAK (BOS)**", "📈"
    elif "choch" in s: return "🔄 **CHANGE OF CHARACTER (CHoCH)**", "⚖️"
    else: return "💡 **ONDER ACADEMY ANALİZ**", "🔍"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data: return {"error": "Veri yok"}, 400
        parite = data.get("parite", "COIN")
        fiyat = data.get("fiyat", "0.0")
        sinyal = data.get("sinyal", "Genel")
        baslik, emoji = tema_olustur(sinyal)
        mesaj = f"{emoji} {baslik}\n---\n💎 **Parite:** #{parite}\n📊 **Detay:** {sinyal}\n📍 **Anlık Fiyat:** {fiyat}\n\n🛡 **KASA DİSİPLİNİ:**\nBu işleme cüzdanın sadece **1/50**'si ile giriniz.\n---\n**Onder Academy**"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"})
        return {"status": "tamam"}, 200
    except Exception as e:
        return {"status": "hata", "message": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
