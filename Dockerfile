FROM python:3.9-slim-bullseye

ARG OPEN_WEATHER_API_KEY="Default_Value"
ENV OPEN_WEATHER_API_KEY=${OPEN_WEATHER_API_KEY}

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]