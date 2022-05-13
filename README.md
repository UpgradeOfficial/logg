# Logg-Backend

The backend api server for the Logg project.

## Project Directory Structure

```bash
Logg
├── accounting
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── appointment
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_appointment_patient.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── constant
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── classes.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── literals.py
│   ├── management
│   │   └── commands
│   │       └── makesuper.py
│   ├── migrations
│   │   └── __init__.py
│   ├── mixins.py
│   ├── models.py
│   ├── modelutils.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── Logg_Backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── ehr
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_patientsocialhistory.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── example.env
├── json
│   ├── accepted_insurance.json
│   ├── available_care.json
│   ├── city.json
│   ├── country.json
│   ├── country_phone_code.json
│   └── state.json
├── manage.py
├── Procfile
├── README.md
├── requirements.txt
├── scripts
│   ├── deploy.sh
│   └── fresh_init.sh
├── templates
│   └── email
│       ├── patient_verification.html
│       └── provider_verification.html
├── twilio_chat
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── user
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py

23 directories, 108 files
```

## Requirements

See the requirements for this project [click here](https://github.com/UpgradeOfficial/logg/blob/main/requirements.txt).

## Installation

- First clone the project into your local machine.

```bash
git clone https://github.com/UpgradeOfficial/logg.git
```

- Go to the repository and create a virtual environment.

```bash
cd Logg
python3 -m venv venv
```

- Activate the virtual environment and install dependencies.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

- Then install wheel, build-essential, python3-dev and psycopg2

```bash
pip install wheel
sudo apt install build-essential
sudo apt install python3-dev
pip install psycopg2
```

- Copy the `example.env` file to `.env` and fill in the values.

```bash
cp example.env .env
```

- The `.env` file should look like this:

```text
SECRET_KEY=your_secret_key
VERSION=v1
DEBUG=True
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=abcd
```

- Create and migrate the database.

```bash
python manage.py migrate
```

## Running the server

- You can run the server with the following command:

```bash
python manage.py runserver
```

- You can also run the server on a custom port by adding the port number after the `runserver` command:

```bash
python manage.py runserver 8000
```
