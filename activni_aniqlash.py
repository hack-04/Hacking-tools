import socket

def get_active_interface_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None

# Test qilish
active_interface_ip = get_active_interface_ip()
print("Active Interface IP:", active_interface_ip)
