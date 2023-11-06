# Set the base image to python:3.12.0-alpine
FROM python:3.12.0-alpine

# Set the working directory to /app
WORKDIR /flask_app

# Copy the current directory contents into the container at /flask_app
COPY . /flask_app

# Install the requirements
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]