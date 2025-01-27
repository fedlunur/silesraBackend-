# Use a specific version of Python
# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container (if it exists)
# COPY requirements.txt .

# # Install the dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the CSM directory into the /app directory inside the container
# COPY csm /app/csm

# # Set the working directory to /app/CSM where manage.py is located
# WORKDIR /app/csm

# # Expose the port the app runs on
# EXPOSE 8000

# # Define the command to start the app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
