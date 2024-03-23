# FastAPI-auth with SqlAlchemy ORM example

This project provides a tutorial example of using the FasAPI-auth library using the SqlAlchemy ORM.
This repository demonstrates the main capabilities of the [library](https://github.com/zayycev22/fastapi-auth).

## What is this for

This repository represents a use-case for using the library.
It shows the basic steps for interacting with the library, including user registration, authentication, serialization,
and checking access permissions.

You can use this project as a guideline for integrating the library into your own project.

# Installation

First of all clone the project

```bash
git clone https://github.com/zayycev22/fastapi_auth_tortoise_example.git
```

Install the library

```bash
pip install auth_fastapi[sqlalchemy]
```

Create .env

```bash
touch .env
```

Generate SECRETE_KEY

```bash
fastapi_auth --generate-key
```

Set the SECRET_KEY environment variable in the .env file with the value you get in previous step

```bash
SECRET_KEY=1234
```

## Docker

If you want to run with docker just run in the console

```bash
docker-compose up --build
```

The server will be available on http://127.0.0.1:8000/docs

## Python

Be careful, library supports python >= 3.10

Run the installation dependencies command

```bash
pip install -r requirements.txt
```

Start the server

```bash
python main.py
```

The server will be available on http://127.0.0.1:8000/docs