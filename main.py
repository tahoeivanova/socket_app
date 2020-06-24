import socket
from views import *

# указываем название функций
URLS = {
    '/': index,
    '/blog': blog
}

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_headers(method, url):
    # если метод не равен методу GET
    if not method == 'GET':
        # возвращаем строку (протокол и версия) и код
        # отделяем заголовки от основного тела ответа
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()


def generate_response(request):
    # нужно распарсить заколовки запроса клиента - ивлечь метод и url
    method, url = parse_request(request)
    # headers (например, google chrome хочет получить заголовки)
    headers, code = generate_headers(method, url)

    # тело ответа
    body = generate_content(code, url)
    return (headers + body).encode()


# установить соединение между клиентом и сервером
# клиент подходит к открытому порту  с запросом - создаем субъекта - того, что принимает запрос
def run():
    # INET - протокол ip 4 версии (4 части, по 1 байту на часть)
    # SOCK_STREAM - TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # доп. параметры - допустить повторное использование адреса - 1 (True)
    server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # связать субъекта с конкретным адресом и портом
    server_socket.bind(('localhost', 8000)) # адрес, число-порт

    # проверить, пришли ли пакеты (дать указание субъекту прослушивать свой порт)
    server_socket.listen()

    # сессия длящаяся, используем бесконечный цикл
    while True:
        # клиент сделал запрос на сервер, наш серверный сокет получил ответ, смотрим ответ
        # сервер что-то получил: accept возвращает кортеж - сокет с другой стороны, адрес сокеты
        client_socket, addr = server_socket.accept()
        # увидеть запрос клиента
        request = client_socket.recv(1024) # кол-во байт в пакете
        print(request)
        # print(request.decode('utf-8'))

        print()
        print(addr)
        # отправить ответ пользователю, принимает request(декодируем)
        response = generate_response(request.decode('utf-8'))

        # ответить клиенту - отправляем 'hello world'
        # но сокеты не понимают строк, только байты, поэтому кодируем
        client_socket.sendall(response)
        # мы в браузере ничего не увидим, пока не закроем соединение
        client_socket.close()




if __name__ == '__main__':
    run()