# Flask + APScheduler — пример с счётчиком

Учебный пример: фоновый планировщик меняет данные каждые 5 секунд, Flask отдаёт их браузеру.

---

## Как это работает (главная идея)

```
[APScheduler]  каждые 5 сек → меняет count (глобальная переменная)
       ↕ общее состояние (глобальная переменная)
[Flask маршрут]  браузер делает запрос → читает count → отдаёт HTML
```

Планировщик и Flask **не знают друг о друге**. Они общаются через общую переменную.

---

## Структура проекта

```
project/
├── site.py
└── templates/
    └── index.html
```

---

## Установка и запуск

```bash
pip install flask flask-apscheduler
python site.py
# Открыть: http://127.0.0.1:5000
```

---

## Ключевые концепции

| Концепция | Зачем |
|---|---|
| `global count` | Без этого Python создаст **локальную** переменную внутри функции и выбросит `UnboundLocalError`. Ключевое слово `global` говорит: "используй переменную из внешней области" |
| Планировщик **не возвращает** HTML | `job1()` — фоновая задача, некому отправлять ответ. Она только **меняет данные** |
| `render_template` только в маршруте | Flask маршрут отвечает на HTTP-запрос браузера — только здесь есть "кому" отдать HTML |
| `<meta http-equiv="refresh">` | Простой способ автообновления страницы для учебных целей |

---

## Типичные ошибки

**`UnboundLocalError: count`** — забыл написать `global count` в функции планировщика.

**`render_template` в задаче планировщика** — планировщик работает вне контекста HTTP-запроса, возвращать HTML некому.

**Страница не обновляется сама** — добавь `<meta http-equiv="refresh" content="5">` в HTML.

## Документация
https://docs-python.ru/packages/modul-apscheduler-python/
https://docs-python.ru/packages/veb-frejmvork-flask-python/rasshirenie-flask-apscheduler/
https://viniciuschiele.github.io/flask-apscheduler/rst/usage.html
