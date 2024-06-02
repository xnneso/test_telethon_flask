from flask import request, Flask, jsonify
import asyncio

from utils.telegram import generate_qr, check_qr, authorized, get_messages, send_message
from utils.wildberries import parse_wb


app = Flask(__name__)
loop = asyncio.get_event_loop()
login_status = False


def background_check_login(login_instance):
    global login_status
    """Фоновая проверка на логин по QR, при авторизации, изменяем глобальную переменную на True"""
    loop.run_until_complete(check_qr(login_instance))
    if loop.run_until_complete(authorized()):
        login_status = True


@app.route('/login', methods=['POST'])
def login():
    login_instance = loop.run_until_complete(generate_qr())
    """Запускаем фоном проверку на логин по QR и отдаём QR юзеру"""
    loop.run_in_executor(None, background_check_login, login_instance)
    return jsonify({'qr_link_url': login_instance.url})


@app.route('/check/login', methods=['GET'])
def check_login():
    """Проверка глобальной переменной login_status"""
    global login_status
    if login_status:
        return jsonify({"status": "login"})
    else:
        return jsonify({"status": "waiting_qr_login"})


@app.route('/messages', methods=['POST', 'GET'])
def get_messages_api():
    if request.method == 'GET':
        """Получаем последние 50 сообщений от пользователя"""
        username = request.args.get('uname')
        result = loop.run_until_complete(get_messages(username))
        return jsonify(result)
    elif request.method == 'POST':
        """Отправляем сообщение пользователю"""
        data = request.json
        result = loop.run_until_complete(send_message(data.get('username'), data.get('message_text')))
        return jsonify(result)


@app.route('/wild', methods=['GET'])
def parse():
    """Парсинг wildberries: любой товар"""
    return jsonify(parse_wb())


if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")
