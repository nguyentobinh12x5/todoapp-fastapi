# TodoApp

This is a simple TodoApp built using FastAPI, PostgreSQL, SQLAlchemy, and JWT for authentication.

## Features

- User Registration: Users can create an account by providing their email and password.
- User Login: Registered users can log in using their credentials.
- Create Task: Authenticated users can create new todo items.
- Update Task: Users can update the status or content of their existing todo items.
- Delete Task: Users can delete their todo items.
- List Task: Users can view a list of their todo items.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nguyentobinh12x5/todoapp-fastapi.git
   ```

2. Navigate to the project directory:

   ```bash
   cd app
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:

   - Create a new database in PostgreSQL.
   - Update the database connection details in the `config.py` file.

5. Run the migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

The API documentation can be accessed at `http://localhost:8000/docs`.

## Authentication

To access the protected routes, you need to include the JWT token in the `Authorization` header of your requests. The token can be obtained by logging in with valid credentials.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
