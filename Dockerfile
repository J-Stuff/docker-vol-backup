FROM python:3.11.9-slim

# Set the working directory
WORKDIR /worker
COPY /src /worker/
COPY /requirements.txt /worker/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Ensure tzdata is installed
RUN apt update && apt install tzdata -y

# Run the container
CMD ["python", "main.py"]