# Logg-Backend

The backend api server for the Logg project.

## Project Directory Structure

```bash
Look In The /*docs*/ folder

```
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
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
