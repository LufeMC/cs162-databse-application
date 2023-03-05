### 1. Answer the following questions with as detail as possible
1. Flask is a Python framework that allows developers to create web servers. It's a microframework because it only provides the essencial tools for creating those servers, and developers can integrate other tools as needed.
   
2.  
	- templates: HTML files that Flask uses to render web applications
	- static files: Images, JavaScript, stylesheets, etc
	- requirements.txt: A file with all the libraries that that specific python application uses along with its versions
	- virtual environment ```venv```: It's a tool that creates separate python environments from the system environment. It will prevent python version conflicts
	- render_template: Function that render the HTML
	- redirect: This function redirects the client
	- url_for: This function generatea a URL for a new view function
	- session: It allows you to store specific information about a client's session
3. 
	- `$ pip3 install -r requirements.txt`: It installs all the specified requirements inside requirements.txt
	- `$ export FLASK_APP=app`: It sets the environment variable FLASK_APP to your app file
	- `$ python3 -m flask run`: Starts the flask server
	
4. - `export FLASK_APP=app.py`: Sets the name of the FLASK_APP to app.py. Then you just need to run python3 -m flask run
   - `python3 app.py`: Run the app.py directly

5. It's important to ensure everyone using the app is following the same version of the libraries used on the app
   
6. The `@app.route` will specify which route the the function is specified to. The default value of the `methods` argument is `['GET']`

7. A decorator is a function that takes another function as input. In Flask, we use it to add functionalities to our view functions.

8. The `config` attribute allows us to modify configuration variables in the application. To define `TESTING=True` or `SECRET_KEY='abc'`, we can use `app.config['TESTING'] = True` and `app.config['SECRET_KEY'] = 'abc'`.


9. JSON stands for JacaScript Object Notation. It's a text-based data format that is easy for humans and machines to read. It's mostly used because it's easier to read and write than XML.


10. The default host of the Flask application is `localhost` or `127.0.0.1` and the default port if `5000`. We can change these values by setting them in the `flask run` command. For example, `flask run --host=0.0.0.0 --port=8000`. Another method, is setting these values inside a `run()` method inside the flask file.