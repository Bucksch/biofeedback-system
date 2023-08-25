# Project Source Code Structure

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