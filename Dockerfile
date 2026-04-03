# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies, prioritizing system dependencies if any are needed
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Run uvicorn server serving app:app on all interfaces (0.0.0.0)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
