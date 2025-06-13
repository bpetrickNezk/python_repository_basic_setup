FROM python:3.13

# Declare environment variables
ENV PATH="/root/.local/bin:$PATH"
# Install uv
RUN apt-get -qq update && apt-get -qq -y install curl graphviz git vim zip htop\
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get -qq -y remove curl \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

# Set the working directory \
WORKDIR /app
