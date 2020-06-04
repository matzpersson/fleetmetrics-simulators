FROM python:3

RUN pip install geopy numpy paho-mqtt

WORKDIR /app
COPY ./simulator ./

CMD [ "python", "./main.py" ]
