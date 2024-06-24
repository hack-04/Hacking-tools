import requests
import re
import urlparse

target_url = "https://google.com"
target_links = []


def extract_link(url):
    response = requests.get(target_url)
    return re.findall(b'(?:href=")(.*?)"', response.content)


def crawl(url):
    href_link = extract_link(url)

    for link in href_link:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(url)


crawl(target_url)

