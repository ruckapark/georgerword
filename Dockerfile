# Use a base Python image
FROM python:3.11-slim

# Install Tkinter (required separately on slim images)
RUN apt-get update && apt-get install -y python3-tk

# Set workdir inside container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Set default command to run GUI
CMD ["python", "app/main.py"]

