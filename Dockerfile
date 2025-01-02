# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install virtualenv and create a virtual environment
RUN pip install --no-cache-dir virtualenv && virtualenv venv

# Install dependencies in the virtual environment
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI app using virtualenv
CMD ["./venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
