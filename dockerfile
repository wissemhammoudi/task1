#Use the official Python base image
FROM python:3.13.1 

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

EXPOSE 8000

# Install the Python dependencies
RUN pip install -r requirements.txt
ENTRYPOINT [ "uvicorn" ]
# Run the FastAPI application using uvicorn server
CMD [ "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
