def run_a_client(group_name = 'mohammad'):
    import json
    import socket
    import threading

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(text):
        sock.send(text.encode('utf-16'))

    HOST, PORT = "localhost", 1379
    sock.connect((HOST, PORT))

    def writing():
        while True:
            text = input()
            send(text)

    def listening():
        while True:
            received = sock.recv(1024)
            print(received.decode('utf-16'))

    threading.Thread(target=writing, daemon=False).start()
    threading.Thread(target=listening, daemon=False).start()

    authen = {
        'password': 123123,
        'group_name': group_name
    }
    authen = json.dumps(authen)
    send(authen)
