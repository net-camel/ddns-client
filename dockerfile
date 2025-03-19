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

RUN (crontab -l 2>/dev/null; echo "30 * * * * python3 /usr/src/app/main.py") | crontab -

VOLUME ["/usr/src/app/log"]

CMD ["crond", "-f"]