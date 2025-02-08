# FastAPI Project with PostgreSQL and Docker

This project is a simple **FastAPI** application connected to a **PostgreSQL** database. The application provides an API to manage questions and choices, and it is containerized using **Docker**. Two types of Docker networks are used: **bridge** and **host**.

## Features

- **FastAPI** for building the web application.
- **PostgreSQL** for data storage.
- API for managing questions and choices.
- Containerized using **Docker**.
- Two Docker network modes used: **bridge** and **host**.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Networking](#networking)

---

## Installation

### Prerequisites


- Docker and Docker Compose
- Python 3.8+
- Git

### Quick Start

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/wissemhammoudi/task.git
cd task
```

### Environment Setup

Create a `.env` file in the project root (e.g., `fastApi/`) with the following structure:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:5432/<database_name>
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=database_name
POSTGRES_HOST=host
```

- For the **bridge network**, the host will be the name of the PostgreSQL container (usually `postgres`).
- For the **host network**, the host will be `localhost` or the IP address of the host machine.

---

## Usage

After the setup is complete, you can run the FastAPI application with Docker and interact with it using the available API endpoints.

The project uses **Docker** for containerization. Docker allows you to run both the FastAPI app and PostgreSQL in isolated environments, ensuring consistency across different machines.

### 1. Build the Docker Image

To build the Docker image for the FastAPI app:

```bash
docker build -t fastapi-postgresql-app .
```

### 2. Run with Docker Compose

You can use **Docker Compose** to manage both the FastAPI app and PostgreSQL database together.

To start the containers:

```bash
docker-compose up --build
```

This command will create two containers: one for FastAPI and one for PostgreSQL. The database will be initialized using the credentials in the `docker-compose.yml` file.

If you have already built the images and just want to start the containers without rebuilding:

```bash
docker-compose up
```

This will start the FastAPI application at `http://localhost:8000`.

---

## API Endpoints

The application provides several endpoints to interact with questions and choices:

### **1. Get Questions**

`GET /question/`

Fetch all available questions.

**Response:**
- **200 OK**: List of questions.

### **2. Create Question**

`POST /question/`

Create a new question. You need to send the question data as a JSON body in the request.

**Request Body Example:**
```json
{
  "question": "What is the capital of France?"
}
```

**Response:**
- **200 OK**: Question created successfully.

### **3. Get Question by Text**

`GET /question/{question_text}`

Get a specific question by its text.

**Example Request:**  
`GET /question/What%20is%20the%20capital%20of%20France`

**Response:**
- **200 OK**: The specific question.
- **422 Unprocessable Entity**: Validation error.

### **4. Delete Question**

`DELETE /question/{question_id}`

Delete a specific question by its ID.

**Example Request:**  
`DELETE /question/1`

**Response:**
- **200 OK**: Question deleted successfully.

### **5. Update Question**

`PATCH /question/{question_id}`

Update a specific question's text.

**Example Request Body:**
```json
{
  "question": "What is the capital of Germany?"
}
```

**Response:**
- **200 OK**: Question updated successfully.

### **6. Get Choices for a Question**

`GET /choice/{question_id}`

Fetch all available choices for a specific question by its ID.

---


## Networking

Two types of Docker networks are used in this project: **bridge** and **host**. We provide two Docker Compose files for different networking setups.

### **Bridge Network (docker-compose.yaml)**

In Docker, a **bridge network** is a default network that is used for communication between containers. When you run `docker-compose`, it sets up a bridge network so that the FastAPI application can communicate with PostgreSQL via a private network.

#### **docker-compose.yaml (Bridge Network)**

```yaml
version: '3.8'

services:
  fastapi:
    image: fastapi-postgresql-app
    container_name: fastapi-container
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    networks:
      - bridge_network

  postgres:
    image: postgres:13
    container_name: postgres-container
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - bridge_network

networks:
  bridge_network:
    driver: bridge

volumes:
  postgres_data:
```

In this configuration:
- The FastAPI container will communicate with the PostgreSQL container using the `bridge_network`.
- Ports are mapped for the FastAPI app (`8000:8000`), and the database uses a persistent volume (`postgres_data`) to store data.

---

### **Host Network (docker-compose-host.yaml)**

The **host network** allows the container to share the network namespace of the host machine. This means that the container uses the host's IP address and ports directly. It is mainly used for performance optimization and when you want the container to bind directly to the host's network interfaces.

#### **docker-compose-host.yaml (Host Network)**

```yaml
version: '3.8'

services:
  fastapi:
    image: fastapi-postgresql-app
    container_name: fastapi-container
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    networks:
      - host_network

  postgres:
    image: postgres:13
    container_name: postgres-container
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - host_network

networks:
  host_network:
    external: true
    name: host

volumes:
  postgres_data:
```

In this configuration:
- The FastAPI and PostgreSQL containers both use the **host network** (`external: true` and `name: host`).
- The containers will not have isolated private network IP addresses, but will share the host’s IP address.

---

### **Which Network to Use?**

- Use the **bridge network** if you want to isolate your containers and ensure they only communicate with each other.
- Use the **host network** if you want containers to directly access your host's network and are not concerned about isolation between containers and the host.

---

