FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright
RUN apt-get update && apt-get install -y default-jre wget && \
    wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz && \
    tar -xvzf allure-2.27.0.tgz -C /opt && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure && \
    rm allure-2.27.0.tgz
RUN playwright install chromium --with-deps

COPY . .

CMD ["pytest", "tests/"]

