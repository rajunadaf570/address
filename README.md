# Address
## Requirements:
1. Python 3.7
2. virtualenv
### Step 1: Create virtualenv and Install requirements.txt file.
    virtualenv -p python3.7 {env_name}
    pip install -r requirements.txt
 Active the virualenv.
### Step 2: Create Migration file, Execute migrations and Run the Application
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

### Create User 
    python manage.py createsuperuser
    
## Api request and response
For api request and response import "address_api.postman_collection.json" using postman.


