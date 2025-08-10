import json
import socket

HOST, PORT = "26.79.83.131", 13372
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    data = sock.recv(1024)
    if not data:
        print("Клиент не получил данных")
        break

    message = json.loads(data.decode())
    if "miss" in message:
        print(message["miss"])
        continue
    elif "msg" in message:
        print(message["msg"])
        user_input = input(">> ")
        sock.sendall(json.dumps({"word": user_input.lower()} if "слово" in message["msg"] else {"letter" : user_input.lower()}).encode())

    elif "state" in message:
        print(
            message["answer"],
            f"Осталось {message['attemps']} попыток\n"
            f"Слово: {message['state']}\n"
            f"Использованные буквы: {', '.join(message['used_letters'])
            }"
        )
