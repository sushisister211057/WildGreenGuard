FROM python:3.10.12-slim

# Update and install python3-pip
RUN apt-get update && \
    apt-get install -y python3-pip

# Create the /app/linebot directory in the container
RUN mkdir -p /app/linebot

# Copy the contents of the local 'linebot' directory to /app/linebot in the container
COPY . /app/linebot

# Set the working directory to /app/linebot
WORKDIR /app/linebot

# Install linebot dependencies
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]