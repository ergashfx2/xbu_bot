FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN sudo mv chromedriver /usr/local/bin/
RUN sudo chmod +x /usr/local/bin/chromedriver
RUN sudo apt update
RUN sudo apt install -y chromium-chromedriver
CMD [ "python", "./app.py" ]
