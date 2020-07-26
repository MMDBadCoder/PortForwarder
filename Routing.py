class RoutManager:
    GroupNameBySocket: dict = {}
    SocketsByGroupName: dict = {}
    PasswordByGroupName: dict = {}

    @staticmethod
    def get_sockets_by_group_name(group_name):
        if not RoutManager.SocketsByGroupName.__contains__(group_name):
            return []
        return RoutManager.SocketsByGroupName[group_name]

    @staticmethod
    def get_adjacent_sockets(socket):
        group_name = RoutManager.GroupNameBySocket[socket]
        return RoutManager.SocketsByGroupName[group_name]

    @staticmethod
    def add_socket_with_group_name(socket, group_name, password):
        if RoutManager.SocketsByGroupName.__contains__(group_name):
            if RoutManager.PasswordByGroupName[group_name] == password:
                RoutManager.SocketsByGroupName[group_name].append(socket)
            else:
                raise Exception('Incorrect password!')
        else:
            if group_name.__len__() < 5:
                raise Exception('So short group name!')
            RoutManager.SocketsByGroupName[group_name] = [socket]
            RoutManager.PasswordByGroupName[group_name] = password
        RoutManager.GroupNameBySocket[socket] = group_name

    @staticmethod
    def remove_a_socket(socket):
        group_name = RoutManager.GroupNameBySocket[socket]
        RoutManager.SocketsByGroupName[group_name].remove(socket)
        if RoutManager.SocketsByGroupName[group_name].__len__() == 0:
            del RoutManager.SocketsByGroupName[group_name]
        del RoutManager.GroupNameBySocket[socket]

    @staticmethod
    def contains(key):
        if key is str:
            return RoutManager.SocketsByGroupName.__contains__(key)
        return RoutManager.GroupNameBySocket.__contains__(key)
