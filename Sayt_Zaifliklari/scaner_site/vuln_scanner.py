import scanner


target_url = "https://apro.uz"
links_to_ignore = ["http://10.0.2.11/dvwa/logout.php"]
data_dict = {"username": "p00194517", "password": "p00194517", "Login": "submit"}


vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post("https://apro.uz/Account/Login?ReturnUrl=%2FHome%2FMain", data=data_dict)
vuln_scanner.crawl()
vuln_scanner.run_scanner()
