# Use official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port FastAPI will run on (default is 8000)
EXPOSE 8000

# Set environment variable for the app to use the .env file
ENV PYTHONUNBUFFERED=1

# Run the app using Uvicorn with worker class "uvicorn.workers.UvicornWorker"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
