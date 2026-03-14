FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt
RUN pip install playwright
RUN apt-get update && apt-get install -y \
    git \
    neovim \
    nodejs \
    npm \
    default-jre \
    wget \
    postgresql \
    postgresql-client \
    && wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz \
    && tar -xvzf allure-2.27.0.tgz -C /opt \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure \
    && rm allure-2.27.0.tgz
RUN playwright install chromium --with-deps
RUN useradd -m -s /bin/bash devuser
RUN git clone https://github.com/chikibambuoni/dotfiles /home/devuser/dotfiles \
    && mkdir -p /home/devuser/.config \
    && ln -s /home/devuser/dotfiles/.config/nvim /home/devuser/.config/nvim \
    && chown -R devuser:devuser /home/devuser/dotfiles /home/devuser/.config
COPY . .
CMD ["pytest", "tests/"]
