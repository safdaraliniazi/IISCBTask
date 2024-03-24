# Use official Python image as base
FROM python:3.8

# Set working directory
WORKDIR /app

# Copy requirements.txt to work directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
