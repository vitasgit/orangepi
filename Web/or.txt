from flask import Flask, request
from RF24 import RF24, RF24_PA_LOW, RF24_1MBPS
import time

app = Flask(__name__)

# Настройки радио
CE_PIN = 73
CSN_PIN = 1
SPI_BUS = 1
radio = None

# Инициализация радио при старте
def init_radio():
    global radio
    try:
        radio = RF24(CE_PIN, CSN_PIN, SPI_BUS)
        if not radio.begin():
            print("ERROR: nRF24L01 не отвечает")
            return False

        radio.setPALevel(RF24_PA_LOW)
        radio.setDataRate(RF24_1MBPS)
        radio.setChannel(76)
        radio.openWritingPipe(b"NODE1")
        radio.stopListening()

        print("✓ nRF24L01 инициализирован")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# Отправка команды
def send_cmd(cmd):
    if radio is None:
        return "ERROR: Радио не инициализировано"

    try:
        if cmd == "on":
            msg = b"LED_ON"
        elif cmd == "off":
            msg = b"LED_OFF"
        else:
            return "ERROR: Неизвестная команда"

        # Отправляем 3 раза для надёжности
        ok = 0
        for i in range(3):
            if radio.write(msg):
                ok += 1
            time.sleep(0.01)

        if ok >= 2:
            return f"OK: Отправлено ({ok}/3)"
        else:
            return f"FAIL: Ошибка отправки ({ok}/3)"
    except Exception as e:
        return f"ERROR: {e}"

# Главная страница с кнопками
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LED Control</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: #f0f0f0;
            }
            h1 { color: #333; }
            button {
                font-size: 20px;
                padding: 20px 40px;
                margin: 10px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                color: white;
            }
            .on { background: #4CAF50; }
            .off { background: #f44336; }
            button:active { transform: scale(0.95); }
            #result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <h1>🔌 LED Control</h1>
        <p>Orange Pi → nRF24L01 → Arduino</p>

        <button class="on" onclick="send('on')">💡 Включить</button>
        <button class="off" onclick="send('off')">🌑 Выключить</button>

        <div id="result"></div>

        <script>
            function send(cmd) {
                fetch('/cmd?action=' + cmd)
                    .then(r => r.text())
                    .then(data => {
                        const result = document.getElementById('result');
                        result.textContent = data;
                        result.className = data.startsWith('OK') ? 'success' : 'error';
                        result.style.display = 'block';
                    })
                    .catch(err => {
                        const result = document.getElementById('result');
                        result.textContent = 'Ошибка: ' + err;
                        result.className = 'error';
                        result.style.display = 'block';
                    });
            }
        </script>
    </body>
    </html>
    '''

# API для отправки команд
@app.route('/cmd')
def command():
    action = request.args.get('action', '')
    result = send_cmd(action)
    return result

# Проверка статуса
@app.route('/status')
def status():
    if radio is None:
        return "ERROR: Радио не инициализировано"
    return "OK: Система работает"

if __name__ == '__main__':
    print("=== Flask nRF24 Server ===")
    init_radio()

    # Запускаем сервер
    # 0.0.0.0 - доступ со всех устройств в сети
    # port=5000 - порт сервера
    app.run(host='0.0.0.0', port=5000, debug=False)
