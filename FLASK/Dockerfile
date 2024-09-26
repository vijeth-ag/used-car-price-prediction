# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY flask_requirements.txt ./
RUN pip install --no-cache-dir -r flask_requirements.txt

# Copy the Flask app code
COPY flask_app.py ./

# Expose the port
EXPOSE 5001

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=50001"]
