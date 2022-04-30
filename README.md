# Ecommerce

# Setup


1. Create virtualenv with python version 3.8 or higher
   
   `virtualenv env_name`
2. Activate virtualenv and install requirements.txt
   ```
    env_name\scripts\activate
    pip install -r requirements.txt
   ```
3. Add your secrets to .env

    ` Ecommerce/.env`
    ```
    NAME=' '
    USER=' '
    PASSWORD=' '
    HOST=' '
    PORT=' '
    ENGINE=' '
    EMAIL_HOST_USER=' '
    EMAIL_HOST_PASSWORD=' '
    
    ```
4. Run commands     
    ```
    python manage.py makemigrations user
    python manage.py migrate
    python manage.py runserver
    ```

5. Visit swagger ui at http://127.0.0.1:8000/
