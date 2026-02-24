from flask import Flask, render_template
from flask_apscheduler import APScheduler

app = Flask(__name__)
count = 0
@app.route("/")
def index():
    return render_template('index.html', count=count)


# экземпляр класса APScheduler
sched = APScheduler()
@sched.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def job1():
    global count  # нужен, когда хочешь изменить внешнюю переменную
    count += 1


if __name__ == '__main__':
    #app = Flask(__name__)

    # SCHEDULER_API_ENABLED: bool, значение по умолчанию: False - включает/отключает API планировщика;
    sched.api_enabled = True
    sched.init_app(app)
    sched.start()
    app.run()
