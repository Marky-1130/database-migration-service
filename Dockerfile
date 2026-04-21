#Base Image
FROM python:3.11-slim

#Working director
WORKDIR /app

# Install the necessary packages
RUN apt-get update -y \
    && apt-get install -y default-libmysqlclient-dev pkg-config build-essential \
    # Remove any unused packages and clear the package list to reduce the image size
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Copy Dependencies
COPY requirements.txt .

#Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of the application
COPY . .

#RUN app
CMD ["bash", "/app/start.sh"]