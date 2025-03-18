FROM alpine:3.21

WORKDIR /usr/src/app
RUN mkdir log

COPY requirements.txt .
RUN apk add python3
RUN apk add py3-pip
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

RUN chmod +x ./main.py

ENV APIKEY=""
ENV SECRET_APIKEY=""

RUN echo -e "#!/bin/sh\npython3 /usr/src/app/main.py" > /etc/periodic/15min/ddns_client
RUN chmod +x /etc/periodic/15min/ddns_client
# RUN echo "*/1 * * * * python3 /usr/src/app/main.py" > crontab
RUN (crontab -l 2>/dev/null; echo "*/1 * * * * python3 /usr/src/app/main.py") | crontab -

CMD ["crond", "-f"]