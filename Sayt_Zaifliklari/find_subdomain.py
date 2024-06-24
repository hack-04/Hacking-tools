import requests


def request(url):
    try:
        return requests.get("https://"+url)

    except requests.exceptions.ConnectionError:
        pass


target_url = "yandex.com"

with open("/home/kali/Downloads/subdomains100.txt", "r") as word_list:
    for line in word_list:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+]Ushbu subdomain mavjud > " + test_url)
