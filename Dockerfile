FROM python:3

RUN pip install geopy numpy paho-mqtt

WORKDIR /usr/src/app
COPY . .

CMD [ "python", "./main.py" ]
