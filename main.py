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
    response_json = response.json()
    return response_json

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
            return False

def update_log(ip, update, status="", message=""):
    time = datetime.now()
    logtime = time.strftime("%m-%d-%Y %H:%M:%S")
    with open("ip.log", "a") as file:
        if update:
            file.write(f"{logtime}    {ip}    updated    {status}    {message}\n")
        else:
            file.write(f"{logtime}    {ip}    not updated    {status}    {message}\n")

public_ip = get_public_ip()

if check_public_ip(public_ip):
    status = update_dns(public_ip)
    if status['status'] != "SUCCESS":
        print("API call failed, check ip.log")
        update_log(public_ip, False, status['status'], status['message'])
    else:
        update_log(public_ip, True, status['status'])
        save_public_ip(public_ip)
else:
    update_log(public_ip, False)

# Since I'm not hitting the porkbun api to check current DNS value, if the value changes from another source this script will not know.
# This code is a mess but works as long as the DNS entry does not change from another source.
# Will refactor this with what I've learned thus far.