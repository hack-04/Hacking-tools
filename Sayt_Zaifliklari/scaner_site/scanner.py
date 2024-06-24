import re
import requests
import urlparse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_link(self, url):
        response = self.session.get(url)
        return re.findall(b'(?:href=")(.*?)"', response.content)

    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_link = self.extract_link(url)

        for link in href_link:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)

        parsed_html = BeautifulSoup(response.content, 'html.parser')
        return parsed_html.find_all("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = form.get("method")
        input_list = form.find_all("input")
        post_data = {}
        for input_tag in input_list:
            input_name = input_tag.get("name")
            input_type = input_tag.get("type")
            input_value = input_tag.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n\n[+] formani testlamoqdamiz " + link)
                is_vulnerable_to_xxs = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xxs:
                    print("\n\n[****] XSS zayiflik mavjud " + link + " ushbu formda \n")
                    print(form)

            if "=" in link:
                print("\n\n[+] Test qilindi " + link)
                is_vuln_to_xxs = self.test_xss_in_link(link)
                if is_vuln_to_xxs:
                    print("\n\n[****] XSS zayiflik mavjud " + link)

    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('test')</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content