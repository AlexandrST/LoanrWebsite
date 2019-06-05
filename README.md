# LoanrWebsite
Simple Django website that allows rentors to post items for rentees to rent, and for rentees to browse rental items

Required dependencies (pip install):
- dj-database-url
- Django
- gunicorn
- psycopg2-binary
- wheel
- whitenoise
- mysqlclient
- Django-credit-cards


Steps to get website running (open a cmd window -> cd into root folder):
- pip install -r requirements.txt <br>
- python manage.py makemigrations
- python manage.py migrate
- python manage.py collectstatic
- python manage.py test # Run the standard tests. These should all pass.
- python manage.py createsuperuser # Create a superuser
- python manage.py runserver
- Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
  - Once admin site is open, add a few ItemTypes (Misc, Electronics, Tools) before proceeding to the main site.
  - Click Register (at the top) to make a new user account
