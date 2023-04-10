# Use an official Python runtime as a parent image
FROM python:3.8-slim
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY *.py /app/
COPY static /app/static/
COPY templates /app/templates/

# Install any needed packages specified in requirements.txt
# RUN pip3 freeze > requirements.txt  // unsure about this line
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=login.py
ENV FLASK_RUN_HOST=0.0.0.0
# ENV Selenium_UseHeadlessDriver=true

# Run login.py when the container launches
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]