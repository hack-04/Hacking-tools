import subprocess
import random
import optparse
import time

print(''' 
   /  |/  /   | / ____/  / ____/ /_  ____ _____  ____ ____  _____
  / /|_/ / /| |/ /      / /   / __ \/ __ `/ __ \/ __ `/ _ \/ ___/
 / /  / / ___ / /___   / /___/ / / / /_/ / / / / /_/ /  __/ /    
/_/  /_/_/  |_\____/   \____/_/ /_/\__,_/_/ /_/\__, /\___/_/     
                                              /____/             
''')


interface = input("interfaceni tanlang: ...")

def changer_mac(inter,new_mac):
    subprocess.call(["ifconfig", inter, "down"])
    subprocess.call(["ifconfig", inter, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", inter, "up"])

# def get_mac():
#     mac = [random.randint(0x00, 0xff) for _ in range(6)]
#     return ':'.join(map(lambda x: "%02x" % x, mac))
def get_mac():
    a = random.randint(100000,999999)
    return a

print("mac manzil doimo o'zgartirilib turiladi")
v = int(input("vaqitni kiriting (sekundda)..."))
print(f"OGOHLANTIRISH: har {v} sekindda mac almashadi")
son = 0
while True:
    try:
        mac = f"000000{get_mac()}"
        changer_mac(interface,mac)
        son+=1
        print(f"Mac_Changer : {son}-marta >>>{mac}")
        time.sleep(v)
    except:
        print("interface xato kiritilgan qayta ishga tushiring")




