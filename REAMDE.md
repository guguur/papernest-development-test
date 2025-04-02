# Papernest API network coverage 📡
This package is a simple API that allows you to check the network coverage of a given address.

## Table of contents 📚

- [Papernest API network coverage 📡](#papernest-api-network-coverage-)
  - [Table of contents 📚](#table-of-contents-)
  - [Environment variables](#environment-variables)
    - [Mandatory variables](#mandatory-variables)
    - [Optional variables](#optional-variables)
  - [Run the API 🚀](#run-the-api-)
    - [Through Docker 🐳](#through-docker-)
    - [Locally 🖥️](#locally-️)
      - [Python version 🐍](#python-version-)
      - [Installation steps 🛠️](#installation-steps-️)
        - [Production](#production)
        - [Development](#development)
      - [Launch the API 🚀](#launch-the-api-)
    - [Test the API](#test-the-api)
  - [Run the tests 🧪](#run-the-tests-)

## Environment variables

Create a `.env` file at the root of the backend. This envirenment variables will be used by `app/env.py` and by the docker compose file.

### Mandatory variables
The variable below is mandatory if you use Docker to run the application. If so, the variable must be set in the `.env` file as follows:
```
# path to the directory of the project
PATH_TO_DIR=/path/to/dir/papernest-development-test
```

### Optional variables 
The variables below are optional. Their default values are set in the `app/env.py` file. You don't have to define them to launch the API. If you want to change them, they are optional and they can be set in the `.env` file as follows:
```
# log level
LOG_LEVEL=INFO
# path to the csv file containing the antennas data
ANTENNAS_DATA_PATH=path_to_antennas_data.csv
# API address URL
API_ADDRESS_URL=http://test-api-address.gouv.fr
```

## Run the API 🚀
There are two ways to run the API: through Docker or locally.

### Through Docker 🐳
You can use the provided `Makefile` to run the API using Docker:
```bash
make up
```
This will build the Docker image and run the API in a container. The API will be available at `http://localhost:8005/docs`.

To stop the container, you can run:
```bash
make down
```

### Locally 🖥️
#### Python version 🐍
3.11 or higher is required to run this package.

#### Installation steps 🛠️

##### Production
Make sure to run this in a dedicated python virtual environment, using your favourite virtual environment manager:
```bash
$ pip install -r requirements.txt
```
If you're familiar with `poetry`, you might consider running instead:
```bash
$ poetry install --no-root
```

##### Development
Additional development dependencies can be installed. They can be retrieved by running:
```bash
$ pip install -r requirements-dev.txt
```
Or again, with `poetry`:
```bash
$ poetry install --with testing,quality --no-root
```
The development dependencies include the testing and quality dependencies. They are used to run the tests and to check the code quality.

#### Launch the API 🚀
To run the API, you can simply run the following command:
```bash
uvicorn app.main:app --reload --port 8005
```
Similarly to the Docker version, the API will be available at `http://localhost:8005/docs`.

### Test the API
You can test the API by sending a POST request to the `/coverage` endpoint with the following payload:
```json
{
	"id1" : "157 boulevard Mac Donald 75019 Paris",
	"id4" : "5 avenue Anatole France 75007 Paris",
	"id5" : "1 Bd de Parc, 77700 Coupvray",
	"id6" : "Place d'Armes, 78000 Versailles",
	"id7" : "17 Rue René Cassin, 51430 Bezannes",
	"id8" : "78 Le Poujol, 30125 L'Estréchure"
}
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
app/env.py                     15      3      0      0    80%
app/load_data.py               13      0      0      0   100%
app/logger.py                   6      0      0      0   100%
app/main.py                     4      0      0      0   100%
app/router.py                   9      0      0      0   100%
app/schemas.py                  6      0      0      0   100%
app/services.py                34      0     12      0   100%
-------------------------------------------------------------
TOTAL                         130      3     14      0    98%
```
