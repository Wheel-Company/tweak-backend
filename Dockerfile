# Use the official Python image as the base image
FROM arm64v8/python:3

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your Django application will run on
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
