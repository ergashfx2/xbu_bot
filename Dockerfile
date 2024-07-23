FROM python:3.9
WORKDIR /app
COPY . /app
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo apt install ./google-chrome-stable_current_amd64.deb
RUN sudo apt-get update
RUN sudo apt-get install -y libnss3 libgconf-2-4 libxss1 libxtst6 libgdk-pixbuf2.0-0

RUN pip install -r requirements.txt
CMD [ "python", "./app.py" ]
