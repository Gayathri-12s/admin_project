# 🎬 FilmStream Backend – Django & MySQL

This repository contains the backend of the FilmStream OTT platform built using Django and MySQL.  
It is responsible for handling business logic, managing movie data, and serving APIs to the frontend.

---

##  Features

- CRUD operations for movie/content management  
- Separate Django apps for modular design (`admin_app`, `user_api`)  
- API endpoints for frontend integration  
- Admin panel using Django Admin  
- MySQL database integration using Django ORM  

---

##  Tech Stack

- Django  
- MySQL  
- Django ORM  

---

##  Project Structure

admin_project/
│
├── admin_app/ # Admin-side functionality
│ ├── migrations/
│ ├── static/
│ ├── templates/
│ ├── models.py
│ ├── views.py
│ ├── admin.py
│ └── apps.py
│
├── user_api/ # User-facing APIs
│ ├── migrations/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ └── apps.py
│
├── admin_project/
│ ├── settings.py # Configuration (MySQL setup)
│ ├── urls.py # Root URL routing
│ ├── asgi.py
│ └── init.py
│
├── manage.py


---

##  API Overview (User API)

The `user_api` app provides endpoints used by the frontend:

- GET /movies → Fetch all movies  
- GET /movies/:id → Fetch movie details  
- POST /movies → Add new movie  
- PUT /movies/:id → Update movie  
- DELETE /movies/:id → Delete movie  


##  Setup Instructions

### 1️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure MySQL Database

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
               }
            }
4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
5️⃣ Run Server
python manage.py runserver
🔗 Related Project

Frontend (React):
  https://github.com/Gayathri-12s/filmstream
