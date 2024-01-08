# My Book Store

## (A FastAPI project for backend of a book store)

Here is a FastApi project for backend of a simple book store.  
This project uses sqlite and SQLAlchemy for the database and has token-base authentication for user and admin
separately.
To use it and test it fallow these instructions:
<br><br>

### 1. Download project

Download the project into your devise or simply clone the project into your virtual environment or any directory
you want by running the
command :

```commandline
git clone https://github.com/HB2102/My-Book-Store
```

### 2. Install requirements

First you should install the requirements of the project, for that, go to the project directory and run the command :

```commandline
pip install -r requirements.requirements.txt
```

and wait for pip to install packages.

### 3. Run the project

For running the project, go to its directory and run the command :

```commandline
uvicorn main:app --reload
```

if you get the error that the port is in use you can change the port by running the command like :

```commandline
uvicorn main:app --reload --port 5000
```

and it'll change the port to 5000 but running it on port 8000 should be fine at the beginning.  
When the project is running you can go to the URL that it shows tou on your browser and see the first page.

### 4. See the APIs list

To see the list of APIs just add /docs at the end of the URL. It should look something like this :

```Url
http://127.0.0.1:8000/docs
```

you can see the list of all the APIs and you can test them if you want. You can create user buy books and use the
system.
You also can do everything you want as an admin. database already has one default admin with default values of :

- Username : admin
- Password : admin

you can login as admin and add books, remove them, promote other users to admin and...
<br><br><br>
Thanks for your time.
