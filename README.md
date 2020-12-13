# factoryworldwide
Repository for factoryworldwide assignment

Installation:

- $ pip install virtualenv
- $ cd factoryworldwide
- $ virtualenv -p python3.7 venv
- $ source venv/bin/activate (or . venv/bin/activate)
- $ pip install -r requirements.txt
- $ echo "$(pwd)" | sudo tee venv/lib/python3.7/site-packages/factoryworldwide_app.pth > /dev/null

Database setup:

- $ cd factoryworldwide_app/server/
- $ export FLASK_APP=migrate.py
- $ flask db init
- $ flask db migrate
- $ flask db upgrade

Run application: 

- navigate to factoryworldwide_app/server/ folder

- $ python RunServer.py

Endpoints:

- Home page: http://127.0.0.1:5000/ [GET]
- User registration: http://127.0.0.1:5000/register [GET, POST]
- User login: http://127.0.0.1:5000/login [GET, POST]
- Create recipe: http://127.0.0.1:5000/create-recipe [GET, POST]
- Get all recipes: http://127.0.0.1:5000/get-recipe [GET]
- Get recipe by id: http://127.0.0.1:5000/get-recipe/1 [GET]
- Get user recipes: http://127.0.0.1:5000/get-user-recipe [GET]
- Get recipes with minimum ingredients: http://127.0.0.1:5000/get-recipe-filter/min [GET]
- Get recipes with maximum ingredients: http://127.0.0.1:5000/get-recipe-filter/max [GET]
- Search recipes: http://127.0.0.1:5000/search-recipe [GET, POST]
- Create Ingredient: http://127.0.0.1:5000/create-ingredient [GET, POST]
- Get 5 most used ingredients: http://127.0.0.1:5000/get-ingredients [GET]
- Get user profile: http://127.0.0.1:5000/get-user-profile [GET]
- Rate recipe: http://127.0.0.1:5000/rate-recipe [POST]

Docker

Pull image from docker hub and run:

- docker pull sergandrex/factoryworldwide:1.0.1
- docker run -p 5000:5000 sergandrex/factoryworldwide:1.0.1

Docker build image from Dockerfile:

- cd factoryworldwide
- docker build -t factoryworldwide:1.0.1 .
- docker run -p 5000:5000 factoryworldwide:1.0.1



