import json
import socket
import socketserver
import threading

from Routing import RoutManager


class ConnectionSocket(threading.Thread):

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def run(self):
        while True:
            try:
                data = self.connection.recv(1024)
                self.handle(data)
            except:
                RoutManager.remove_a_socket(self)
                return

    def handle(self, data):
        try:
            if RoutManager.contains(self):
                self.handle_an_authenticated_user_message(data)
            else:
                self.handle_new_user_message(data)
        except Exception as e:
            self.send_response(str(e), encode=True)

    def handle_new_user_message(self, data):
        try:
            data = data.decode('utf-16')
            data = json.loads(data)

            group_name = data['group_name']
            password = data['password']
        except:
            raise Exception('Bad format of authenticated message!')

        try:
            RoutManager.add_socket_with_group_name(self, group_name=group_name, password=password)
        except Exception as e:
            self.send_response(str(e), encode=True)
            return

        self.send_response('ACCEPT', encode=True)

    def handle_an_authenticated_user_message(self, data):
        for socket in RoutManager.get_adjacent_sockets(self):
            try:
                socket.send_response(data=data, encode=False)
            except:
                RoutManager.remove_a_socket(socket)

        group_name = RoutManager.GroupNameBySocket[self]
        short_text = data[:30].decode('utf-16') + '...'
        print(group_name + ':', short_text)

    def send_response(self, data, encode):
        if encode:
            self.connection.send(data.encode('utf-16'))
        else:
            self.connection.send(data)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":

    s = socket.socket()
    port = 1379
    s.bind(('', port))
    s.listen(5)

    while True:
        connection, addr = s.accept()
        connection_socket = ConnectionSocket(connection)
        connection_socket.start()
