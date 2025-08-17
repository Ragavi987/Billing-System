Super User Credential:

user name : ragavi

email : ragavim@gmail.com

password : admin123

Project Structure:


billing_system/                   <-- Project Root
│
├── billing_system/               <-- Project Folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── billing/                      <-- Our App
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/                <-- Templates Folder
│   │   └── billing/
│   │       ├── billing_form.html
│   │       └── billing_result.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── manage.py
└── requirements.txt
