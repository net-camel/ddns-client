from datetime import datetime
import os
import requests
import json

api_key = os.getenv("APIKEY")
secret_api_key = os.getenv("SECRETAPIKEY")

def update_dns(ip):
    url = "https://api.porkbun.com/api/json/v3/dns/editByNameType/netcamel.com/A/"
    payload = json.dumps({
        "apikey": api_key,
        "secretapikey": secret_api_key,
        "content": ip
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    return response

def get_public_ip():
    url = "http://ipv4.icanhazip.com"
    response = requests.request("GET", url)
    ip = response.text
    return ip.strip() # strip newlines

# Update DNS if true
def check_public_ip(ip):
    previous_ip = read_public_ip()
    if ip == previous_ip:
        return False
    else:
        return True

def save_public_ip(ip):
    with open("public_ip", "w") as file:
        file.write(ip)

def read_public_ip():
    while True:
        try:
            with open("public_ip", "r") as file:
                ip = file.read()
                return ip
        except:
            print("No public_ip file found, saving current IP")
            public_ip = get_public_ip()
            save_public_ip(public_ip)

def update_log(ip, update):
    time = datetime.now()
    logtime = time.strftime("%m-%d-%Y %H:%M:%S")
    with open("ip.log", "a") as file:
        if update:
            file.write(f"{logtime}    {ip}    updated\n")
        else:
            file.write(f"{logtime}    {ip}    not updated\n")

public_ip = get_public_ip()

if check_public_ip(public_ip):
    save_public_ip(public_ip)
    update_dns(public_ip)
    update_log(public_ip, True)
else:
    update_log(public_ip, False)

# Need to check for status code returned from API for errors. Note errors in ip.log