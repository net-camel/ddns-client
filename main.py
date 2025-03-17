from datetime import datetime
import os
import requests
import json
import logging
from typing import Dict, Any, Optional, Tuple

# Logging config
logging.basicConfig(
    filename="ddns.log",
    level=logging.INFO,
    format="%(asctime)s    %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S"
)
logger = logging.getLogger("ddns_client")

# Constants
IP_CHECK_ENDPOINT = "https://ipv4.icanhazip.com"
DNS_CHECK_ENDPOINT = "https://api.porkbun.com/api/json/v3/dns/retrieveByNameType"
DNS_EDIT_ENDPOINT = "https://api.porkbun.com/api/json/v3/dns/editByNameType"
DOMAIN = "netcamel.com"
RECORD_TYPE = "A"

class DDNSClient:
    def __init__(self, domain: str, record_type: str):
        """Initialize with API keys and domain information"""
        self.api_key = os.getenv("APIKEY")
        self.secret_api_key = os.getenv("SECRETAPIKEY")
        self.domain = domain
        self.record_type = record_type

        if not self.api_key or not self.secret_api_key:
            raise ValueError("API keys not found in environment variables")
        
    def get_public_ip(self) -> str:
        """Get current public IP"""
        try:
            response = requests.get(IP_CHECK_ENDPOINT, timeout=10)
            response.raise_for_status()
            return response.text.strip() # Strip newlines
        except requests.RequestException as e:
            logger.error(f"Failed to get public IP: {e}")
            raise

    def get_dns_record(self) -> str:
        """Get DNS record IP address"""
        url = f"{DNS_CHECK_ENDPOINT}/{self.domain}/{self.record_type}/"

        payload = {
            "apikey": self.api_key,
            "secretapikey": self.secret_api_key
        }

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"DNS check request failed: {e}")
            return f"HTTP error: {str(e)}"
        try: # Grab IP from api response
            ip_address = response.json()
            return ip_address['records'][0]['content']
        except KeyError as e:
            logger.error(f"DNS check content return failed at key: {e}")
            return f"KeyValue error: {str(e)}"
        
    def compare_ips(self, public_ip: str, dns_ip: str) -> bool:
        """Compare public IP with DNS entry IP, return true if same"""
        if public_ip == dns_ip:
            logger.info(f"Public IP: {public_ip}, DNS IP: {dns_ip}. \
                        Values match, not updating DNS")
            return True
        else:
            logger.info(f"Public IP: {public_ip}, DNS IP: {dns_ip}. \
                        Values differ, updating DNS")
            return False
            
    def update_dns(self, public_ip: str) -> None:
        pass


    def run(self) -> None:
        public_ip = self.get_public_ip()
        dns_ip = self.get_dns_record()

if __name__ == "__main__":
    pass

# Finish update_dns method
# Finish run method
# Create main function
# How can I test this code?