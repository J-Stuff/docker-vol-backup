FROM python:3.11.9-slim

# Set the working directory
WORKDIR /worker
COPY /src /worker/
COPY /requirements.txt /worker/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Run the container
CMD ["python", "main.py"]