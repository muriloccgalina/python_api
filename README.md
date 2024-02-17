# Instructions

## Configuration and Execution

### Installing the libs

First of all, you must download the libs necessary to run the project.

```sh
pip install flask
pip install flask-marshmallow
pip install flask-sqlalchemy
pip install flask-migrate
pip install mashmallow-sqlalchemy
```

### Environment Setup

Before starting the application, you need to set up some environment variables for Flask. Run the following commands in the terminal:

```sh
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
```

This sets the Flask application as `app`, sets the environment to development, and activates the debug mode.

### Running the Application

To start the Flask development server, run the following command in the terminal:

```sh
flask run --host=localhost --port=8080
```

This will start the Flask application on `localhost` (127.0.0.1) at port `8080`. You can access the application in your browser by visiting `http://localhost:8080`.

## Database Migrations Setup and Execution

If you are using database migrations with Flask-Migrate, follow these steps:

### Initializing the Database

So first you must configure your database in the **__init__.py** file:

```sh
app.config['SQLALCHEMY_DATABASE_URI'] = "Your database"
```

Before running migrations, you need to initialize the migration system. Run the following command in the terminal:

```sh
flask db init
```

This will create a `migrations` directory in your Flask project to store database migrations.

### Creating Migrations

After initializing the migration system, create an initial migration based on the current data model. Run the following command in the terminal:

```sh
flask db migrate
```

This will create a migration file containing the necessary changes to reflect the current state of the data model.

### Applying Migrations

Finally, apply the migrations to the database. Run the following command in the terminal:

```sh
flask db upgrade
```

This will apply all pending migrations to the database, updating it to the latest version of the data model.
