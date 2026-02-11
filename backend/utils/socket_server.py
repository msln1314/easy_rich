import json
import socket
import threading


class SocketServer:
    """
    socket server 操作
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 3636, send_type: str = "tcp"):
        """
        :param host: socket server 地址
        :param port: socket server 端口
        :param send_type: 通信协议
        """
        self.send_type = send_type
        if self.send_type == "tcp":
            socket_type = socket.SOCK_STREAM
        elif self.send_type == "udp":
            socket_type = socket.SOCK_DGRAM
        else:
            print("不支持通信协议")
            raise ValueError("不支持的通信协议")
        self.server_socket = socket.socket(socket.AF_INET, socket_type)
        self.host = host
        self.port = port
        self.client_connections = {}
        self.listen()

    # 处理客户端连接的线程函数
    def handle_client(self,client_sock, client_address):
        print(22222222222223)
        try:
            # 将客户端连接信息保存到字典中
            # 接收客户端请求数据
            cmd = '{"A01":110000,"A02":110000,"A03":110000}'
            uncmd = '{"A01":100000,"A02":100000,"A03":100000}'
            print(uncmd)
            client_sock.send(uncmd.encode())
            data = client_sock.recv(1024)
            request = data.decode('utf-8', 'ignore')
            print('Received request from {}: {}'.format(client_address, request))

            # 处理请求（这里只是一个示例）
            if request == 'send_command':
                # cmd = '{"A01":110000,"A02":110000,"A03":110000,"A04":110000,"A05":110000,"res":"123"}'
                cmd = '{"A01":110000,"A02":110000,"A03":110000}'
                uncmd = '{"A01":100000,"A02":100000,"A03":100000}'
                self.send_command_to_client(client_address, cmd)
                response = 'Command sent to client'
            else:
                response = 'Invalid request'

            client_sock.sendall(response.encode())
        finally:
            print('2')
            # 关闭客户端连接
            # client_sock.close()
            # del self.client_connections[client_address]
            # print('Client {} connection closed.'.format(client_address))

    # 向特定客户端发送指令
    def send_command_to_client(self,client_address, command):
        print(self.client_connections,"cllienet")
        if client_address in self.client_connections:
            client_sock = self.client_connections[client_address]
            client_sock.sendall(command.encode())
    def listen(self):
        # 绑定服务器地址和端口
        server_address = (self.host, self.port)
        self.server_socket.bind(server_address)
        # 监听客户端连接
        self.server_socket.listen(5)
        print('Server is listening on {}:{}'.format(*server_address))

        while True:
            # 等待客户端连接
            print('Waiting for a client connection...')
            client_sock, client_address = self.server_socket.accept()
            print('Client connected:', client_address)
            self.client_connections[client_address] = client_sock

            # 创建一个新的线程来处理客户端连接
            client_thread = threading.Thread(target=self.handle_client, args=(client_sock, client_address))
            # 设置成守护线程
            # client_thread.setDaemon(True)
            client_thread.start()



if __name__ == '__main__':
    _host = "0.0.0.0"
    _port = 50000
    cmd ='{"A01":100000,"A02":100000,"A03":100000}'

    SS = SocketServer(host=_host,port=_port)
    SS.send_command_to_client('192.168.123.18',cmd)

