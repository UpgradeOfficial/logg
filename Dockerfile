FROM python:3.9-slim-bullseye
WORKDIR /Logg-Backend
COPY . .
# Install dependencies:
RUN pip install -r requirements.txt
RUN pip install wheel
RUN pip install psycopg2-binary
# Migrate
RUN python manage.py migrate
# Start server
CMD ["python", "manage.py","runserver", "0.0.0.0:80"]
