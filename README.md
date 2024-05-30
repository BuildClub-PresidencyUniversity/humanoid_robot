Let's create a Flask application that uses your `GeminiChatbot` class to handle incoming questions and return responses in JSON format. We'll include the necessary Docker configuration to ensure everything runs smoothly in a containerized environment.


### `requirements.txt`
Include all the dependencies needed for your project. Example:
```
Flask==2.0.1
python-dotenv==0.19.0
google-generativeai
requests
```

### `Dockerfile`
```Dockerfile
# Use a Python 3.10 image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy specific files to the container
COPY .env .
COPY offline_ai.py .
COPY hostedAI.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "hostedAI.py"]
```

### `.env`
Make sure to create a `.env` file with your Google API key.
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Building and Running the Docker Container
1. Build the Docker image:
   ```sh
   docker build -t gemini-chatbot .
   ```

2. Run the Docker container:
   ```sh
   docker run -d -p 5000:5000 --name gemini-chatbot-container gemini-chatbot
   ```

### Testing the Flask App
You can test the Flask app by sending a POST request to `http://<host_ip>:5000/chat` with a JSON body. Example using `curl`:
```sh
curl -X POST http://<host_ip>:5000/chat -H "Content-Type: application/json" -d '{"input_text": "Do You know about lord Sri Krishna"}'
```

This setup will allow you to run your Flask-based chatbot globally using Docker, with all necessary dependencies and configurations.