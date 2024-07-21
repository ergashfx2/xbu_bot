FROM python:latest
WORKDIR /app
COPY . /app
RUN apt update
RUN apt upgrade
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN pip install -r requirements.txt
CMD [ "python", "./app.py" ]
