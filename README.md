# ddns-client
Used to update site's DNS record with current public IP using Porkbun API

## Installation
Use the below Docker Compose file to get started:
```
services:
  ddns_client:
    image: netcamel/ddns_client:latest
    volumes:
      - ./:/usr/src/app/log
    environment:
      - APIKEY=
      - SECRETAPIKEY=
```