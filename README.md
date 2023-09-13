# flask-app
Follow these steps to get the app running on your local machine:
1. Create a folder to to contain the project and go to that directory in your editor/IDE
2. Create a Python virtual environment
   - https://docs.python.org/3/tutorial/venv.html
3. Download dependencies and set environment variables
   - Open a terminal in your project folder
   - Run "pip install flask"
   - Run set FLASK_APP=app (export instead of set for non-Windows)
   - Run set FLASK_ENV=development (export instead of set for non-Windows)
4. Run the app
   - In the command line, run "flask run"
   - You should get an output similar to:
     -  * Debug mode: off     
        **WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.**
        * Running on http://127.0.0.1:5000
        Press CTRL+C to quit
   - Copy the link and paste into your browser
