# Papernest API network coverage 📡
This package is a simple API that allows you to check the network coverage of a given address.

## Table of contents 📚

- [Papernest API network coverage 📡](#papernest-api-network-coverage-)
  - [Table of contents 📚](#table-of-contents-)
  - [Run the API 🚀](#run-the-api-)
    - [Through Docker 🐳](#through-docker-)
    - [Locally 🖥️](#locally-️)
      - [Python version 🐍](#python-version-)
      - [Installation steps 🛠️](#installation-steps-️)
        - [Production](#production)
        - [Development](#development)
      - [Launch the API 🚀](#launch-the-api-)
  - [Run the tests 🧪](#run-the-tests-)

## Run the API 🚀
There are two ways to run the API: through Docker or locally.

### Through Docker 🐳
You can use the provided `Makefile` to run the API using Docker:
```bash
make up
```
This will build the Docker image and run the API in a container. The API will be available at `http://localhost:8005`.

To stop the container, you can run:
```bash
make down
```

### Locally 🖥️
#### Python version 🐍
3.11 or higher is required to run this package.

#### Installation steps 🛠️

##### Production
Make sure to run this in a dedicated python virtual environment, using your favorite virtual
environment manager:
```bash
$ pip install -r requirements.txt
```
If you're familiar with `poetry`, you might consider running instead:
```bash
$ poetry install --no-root
```
It is still recommended to run:
```bash
$ pip install -r requirements.txt
```
Afterwards to make sure all the required dependencies will be installed.

##### Development
Additional development dependencies can be installed. They can be retrieved by running:
```bash
$ pip install -r requirements-dev.txt
```
Or again, with `poetry`:
```bash
$ poetry install --with testing,quality --no-root
```
The development dependencies include the testing and quality dependencies. They are used to run the 
tests and to check the code quality.

#### Launch the API 🚀
To run the API, you can simply run the following command:
```bash
uvicorn app.main:app --reload --port 8005
```

## Run the tests 🧪
To run the tests, you have to install the development dependencies as explained in the [Installation steps](#installation-steps-️) section.

Then, you can run the tests using the following command:
```bash
pytest
```

To run the tests with coverage report, you can run:
```bash
poetry run coverage run -m pytest
poetry run coverage report
```

Example of coverage report:
```
Name                        Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------
app/api_address/client.py      23      0      2      0   100%
app/constants.py               20      0      0      0   100%
app/logger.py                   5      0      0      0   100%
app/main.py                     4      0      0      0   100%
app/router.py                  13      0      0      0   100%
app/schemas.py                  6      0      0      0   100%
app/services.py                34      0     12      0   100%
-------------------------------------------------------------
TOTAL                         105      0     14      0   100%
```
