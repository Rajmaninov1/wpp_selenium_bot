FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    default-jre \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# # Download and install the browser (e.g., Chrome) and its driver
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update && apt-get install -y google-chrome-stable \
#     && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
#     && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
#     && rm /tmp/chromedriver.zip


# RUN pip install selenium


# EXPOSE 4444 

# Set up your Python application
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .

EXPOSE 8000
# EXPOSE 4444
 
# Start Selenium Grid and your Python app
CMD ["bash", "python3 main.py"]