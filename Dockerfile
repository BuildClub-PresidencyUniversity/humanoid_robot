# Use a Python 3.10 image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements_forDocker.txt .
RUN pip install --no-cache-dir -r requirements_forDocker.txt

# Copy specific files to the container
COPY .env .
COPY online_ai.py .
COPY hostedAI.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "hostedAI.py"]
