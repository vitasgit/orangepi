from flask import Flask, render_template, request
from RF24 import RF24, RF24_PA_LOW, RF24_250KBPS, RF24_DRIVER
from flask_apscheduler import APScheduler
import time


app = Flask(__name__)
sched = APScheduler()

def job1():
    send_cmd("1")

def job2():
    send_cmd("0")


def send_cmd(cmd):
    if cmd == "1":
        data = b"\x01"
    elif cmd == "0":
        data = b"\x00"
    
    res = radio.write(data)
    # не работает(всегда false), нужно проверить auto-ack 
    #if res:
    #    print(data, "OK")
    #else:
    #    print(data, "ошибка")

    time.sleep(1)
    return res


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        cmd = request.form.get('submit')  # обращаемся к полю submit (name="submit")
        #cmd = request.form['submit']  # обращаемся к полю как к ключу словаря
        #print(cmd)  # отладка
        send_cmd(cmd)
        
    return render_template('index.html')


@app.route("/timer", methods=["POST", "GET"])
def timer_on():
    if request.method == "POST":
        print("ЗАДАЧИ")  # отладка
        print(sched.get_jobs())

        # исправить 
        if request.form.get('turn_off'):
            try:
                sched.remove_all_jobs()
                print(sched.get_jobs())
            except:
                return
        
        t_on = request.form.get('time_on')
        t_off = request.form.get('time_off')

        h_on = int(t_on.split(":")[0])  # делаем сплит, а потом берем первое значение
        m_on = int(t_on.split(":")[1])  # делаем сплит, а потом берем второе значение
        h_off = int(t_off.split(":")[0])
        m_off = int(t_off.split(":")[1])
        print(t_on)  # отладка
        print(t_off)  # отладка

        # sched.add_job(<id>,<function>, **kwargs)
        # исправить
        try:
            sched.remove_all_jobs()
        except:
            sched.add_job('job_1', send_cmd, trigger='cron', hour=h_on, minute=m_on, args=['1'])  # включение
            sched.add_job('job_2', send_cmd, trigger='cron', hour=h_off, minute=m_off, args=['0'])  # выключение

        print(sched.get_jobs())
        
    return render_template('timer.html')



if __name__ == '__main__':
    CE_PIN = 73  # pin 7 на плате
    CSN_PIN = 11  # для spidev1.1
    pipe1_addr = b"1Node"
    radio = RF24(CE_PIN, CSN_PIN)

    if not radio.begin():
        print("радиомодуль не подключен")
        #exit()
        
    radio.setPALevel(RF24_PA_LOW)        # мощность передатчика (low = -12 dBm)
    radio.setDataRate(RF24_250KBPS)      # Скорость передачи данных, чем меньше - тем дальше (скорость приема и передачи должна быть одинаковая)
    radio.setAutoAck(1);                 # режим подтверждения приёма, 1 вкл 0 выкл
    radio.setRetries(0, 15);             # (время между попыткой достучаться, число попыток) 15 - максимальное
    radio.setPayloadSize(1);             # пакет данных размером 1 байт (бубу передавать 1 или 0)
    radio.setChannel(76)                 # выбираем канал передачи данных с самыми низкими помехами
    radio.powerUp();                     # режим передачи (повышенного потребления), powerDown - режим ожидания
    radio.openWritingPipe(pipe1_addr);   # открыть канал на отправку
    radio.stopListening()                # режим передачи

    sched.api_enabled = True
    sched.init_app(app)
    sched.start()
    print(sched.get_jobs())  # список задач

    app.run(host='0.0.0.0', port=5000, debug=False)
