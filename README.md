# Bio-Feedback System Prototype - Seminar Thesis for Positive Information Systems

## Project Source Code Structure

The following directory structure outlines the organization of this project's source code (`src` directory).

1. **processing:** Contains modules related to signal loading and processing functionality.

   - **ecg:** Future modules for processing electrocardiogram (ECG) signals. Nothing meaningful implemented yet.

     - **ecg_signal.py:** Handles ECG signal processing and analysis.

   - **eda:** Modules for processing electrodermal activity (EDA) signals.

     - **eda_signal.py:** Handles EDA signal processing and feature extraction.

   - **signal.py:** Defines the base `Signal` class for signal processing.

2. **static:** Stores static assets for the web application's frontend.

   - **icons:** Contains SVG icons used for graphical elements.
   - **media:** Stores media files, such as images.
   - **main.css:** Stylesheet for the frontend's visual styling.
   - **main.js:** JavaScript file for client-side interactivity.

3. **templates:** Contains HTML templates for rendering frontend views.

   - **index.html:** Main HTML template for the web application's frontend.

4. **tests:** Houses test-related code and test cases.

   - **test_load_signal.py:** Contains test cases for the `load_signal` functionality.

5. **app.py:** Main application module defining the Flask web app, routes, and interactions.

6. **database.py:** Manages database interactions, including connecting to PostgreSQL and data insertion.

Each component in this structure serves a specific purpose, contributing to the organization and functionality of this software prototype.

## Running the Prototype

To run the prototype of your application, follow the steps outlined below. This guide assumes that you have the required dependencies installed and you are using a PostgreSQL database.

### Step 1: Install Poetry

Ensure you have Poetry, a Python dependency management tool, installed on your system. If not, you can install it using the following command:

```bash
pip install poetry
```

### Step 2: Install Project Dependencies

Navigate to the root directory of your project (where `pyproject.toml` is located) using the terminal. Run the following command to install the project dependencies:

```bash
poetry install
```

Poetry will set up a virtual environment for your project and install the necessary dependencies.

## Step 3: PostgreSQL Server Setup

Make sure your PostgreSQL server is running. You'll need the database name, username, and password for your configuration and, if you want to run the prototype out-of-the-box, a table "eda_parameters" with three columns feature, value, created_at. Update the `get_database_connection()` function in `database.py` with your database details.

To start the PostgreSQL Server, run:

```bash
sudo service postgresql start
```

To log into your PostgreSQL Server, run:

```bash
sudo -u postgresql psql
```

Type "\dt" to see all of your tables and use SQL-commands to create your table.

## Step 4: Start the Flask Application

As soon as your server is up and running, you can launch the Flask application by running the following command:

```bash
poetry run python3 app.py
```

Executing this command will start the Flask development server, making your application accessible locally.

## Step 5: Access the Web Application

Open your web browser and enter the following URL:

```bash
http://127.0.0.1:5000/
```

This will take you to the frontend of the web application. It should display visualizations and extracted features based on the processed EDA signal data. Please note that this is a prototype, and you can enhance and refine your application's functionality and user interface according to your needs.
