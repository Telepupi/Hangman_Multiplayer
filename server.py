import json
import socket
import game_logic
import configparser

class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host : str = "0.0.0.0", port = 8080):
        self.host = host
        self.port = port
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

    def send_data(self, conn, data: dict) -> None:
        message = json.dumps(data).encode("utf-8")
        conn.sendall(message)

    def receive_data(self, conn: socket):
        data = conn.recv(1024)
        if not data:
            print("Сервер не получил данные")
            return None
        return json.loads(data.decode("utf-8"))

    def game_loop(self):

        conn1, addr1 = self.server_socket.accept()
        print("Игрок 1 подключен")
        conn2, addr2 = self.server_socket.accept()
        print("игрок 2 подключен")

        self.send_data(conn1, {"msg":"Введите слово"})
        data = self.receive_data(conn1)
        if data is None:
            print("Сервер не получил слово")
            return
        word = data["word"].lower()

        game = game_logic.GameLogic(word)

        while game.attemps > 0:
            while True:
                self.send_data(conn2, {"msg": "Введите букву"})
                data = self.receive_data(conn2)
                if data is None:
                    self.send_data(conn2, {"miss": "Вы не ввели букву"})
                    continue
                elif len(data["letter"]) != 1:
                    self.send_data(conn2, {"miss": "Ошибка: введите 1 букву"})
                    continue
                else:
                    break
            letter = data["letter"].lower()

            match (game.guess_letter(letter)):
                case 1:
                    game.answer = "Повтор буквы\n"
                case 2:
                    game.answer = "Верно\n"
                case 3:
                    game.answer = "Неверно\n"
            game_state = {
                "answer" : game.answer,
                "state": "".join(l if l in game.guesses else "_" for l in game.word),
                "guesses": list(game.guesses),
                "used_letters": list(game.used_letters),
                "attemps": game.attemps,
                "word": game.word
            }

            self.send_data(conn1, game_state)
            self.send_data(conn2, game_state)

            if "_" not in game_state["state"]:
                self.send_data(conn1, {"msg" : "Отгадывающий победил"})
                self.send_data(conn2, {"msg" : "Вы победили"})
                break
        else:
            self.send_data(conn1, {"msg": "Вы победили"})
            self.send_data(conn2, {"msg": "Загадывающий победил"})

config = configparser.ConfigParser()
config.read("config.ini")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = config["server"]["HOST"].strip()
PORT = int(config["server"]["PORT"])

srv = Server(HOST, PORT)
srv.game_loop()


