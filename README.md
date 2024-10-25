# E-Commerce API

This is a RESTful API built with FastAPI for managing products in an e-commerce application. The API allows users to perform CRUD operations on product data stored in an SQLite database.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create, read, update, and delete products.
- Retrieve a list of all products or specific product details.
- Error handling for API requests and database operations.
- Unit tests for all routes to ensure functionality.

## Installation

### Prerequisites

- Python 3.7 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/howdyrahuldev/e-comm-app.git
   cd e-commerse-application
   
2. Set up the virtual environment and install dependencies:
    ```bash
   poetry install
3. Create the database using Alembic:
    ```bash
   poetry run alembic upgrade head

## Usage

### Running the API

To start the FastAPI server, run:

    poetry run uvicorn src.e_comm_app.app.main:app --reload

The API will be accessible at http://127.0.0.1:8082.

### Swagger Documentation

The automatically generated documentation can be found at:

- [Swagger UI](http://127.0.0.1:8082/docs)
- [ReDoc](http://127.0.0.1:8082/redoc)

## API Endpoints

### Products Endpoints

- **GET** `/v1/products` - Retrieve a list of all products.
- **GET** `/v1/products/{id}` - Retrieve details of a specific product by its ID.
- **POST** `/v1/products` - Create a new product.
  - **Request Body**:
    ```json
    {
      "title": "Product Title",
      "description": "Product Description",
      "price": 100.0
    }
    ```
- **PUT** `/v1/products/{id}` - Update an existing product.
- **DELETE** `/v1/products/{id}` - Delete a product by its ID.

### Users Endpoints

- **POST** `/v1/users/get_token` - Retrieves a bearer token.
- **POST** `/v1/users/register` - Register a user.
  - **Request Body**:
    ```json
    {
      "username": "<username>",
      "password": "<password>",
      "email": "<email>"
    }
    ```
- **PUT** `/v1/users/change-password` - Change current password.
  - **Request Body**:
    ```json
    {
      "username": "<username>",
      "current_password": "<current_password>",
      "new_password": "<new_password>"
    }
    ```

## Running Tests

To run the unit tests for the API, use the following command:
```bash
   poetry run pytest

