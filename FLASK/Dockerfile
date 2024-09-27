# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY flask_app.py ./

COPY model ./model

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=flask_app.py
ENV PYTHONPATH=/usr/local/bin/python3

# Expose the port
EXPOSE 5001

CMD ["python3", "flask_app.py"]
