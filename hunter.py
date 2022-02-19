import requests
from datetime import datetime as dt
from time import sleep
from fake_creds import FAKE_USERNAMES
import random
import threading


NO_OF_THREADS = 20     # No. of thread to run in parallel
PAUSE = 1             # Delay between consecutive requests in each thread (in seconds)



REQUESTS_COUNT = 0
ERROR_COUNT = 0
phis_url = "https://anjalio.000webhostapp.com"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

def submit_fake_credentials(username, passwd, mobile):
    global phis_url
    global headers
    s = requests.Session()

    r = s.get(phis_url, headers=headers)

    form_data = {
        "Username": username,
        "Password": passwd,
        "Mobile": mobile
    }

    r = s.post(phis_url, data=form_data, headers=headers)

    return r.status_code


def generate_fake_cred():
    global FAKE_USERNAMES
    fake_username = random.choice(FAKE_USERNAMES)
    symbol = random.choice(["", "@", "#", "$", "%", "&"])
    fake_passwd = random.choice(FAKE_USERNAMES) + symbol + str(random.randint(1000, 9999))
    fake_mobile = random.choice(["6", "7", "8", "9", "+91 6", "+91 7", "+91 8", "+91 9"]) + str(random.randint(100000000, 999999999))
    return fake_username, fake_passwd, fake_mobile


def main():
    global REQUESTS_COUNT
    global ERROR_COUNT
    
    while 1:
        fake_username, fake_passwd, fake_mobile = generate_fake_cred()
        status_code = submit_fake_credentials(fake_username, fake_passwd, fake_mobile)
        REQUESTS_COUNT += 1
        print(f"{REQUESTS_COUNT} - {status_code} - {fake_username} - {fake_passwd} - {fake_mobile}")
        sleep(5)
        if status_code != 200:
            ERROR_COUNT += 1
            print("HTTP Error: {}".format(status_code))
            quit()
        
        if ERROR_COUNT > 50:
            print("Too many errors. Exiting...")
            break



if __name__ == "__main__":

    threads_list = [threading.Thread(target=main, daemon=True) for _ in range(NO_OF_THREADS)]
    for thread in threads_list:
        thread.start()
    
    try:
        while True:
            sleep(2)
    except KeyboardInterrupt:
        quit()