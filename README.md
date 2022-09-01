# grad API

## Setup
Install Python
- Install [Python](https://www.python.org/downloads/) (version 3.10).

Main frameworks and packages: 
- [FastAPI](https://fastapi.tiangolo.com/)

## Set and activate virtual environment
In project folder, execute the following commands:

```bash
pip install pipenv
export PIPENV_VENV_IN_PROJECT="enabled"
mkdir .venv
pipenv shell
source .venv/Scripts/activate
```

## Install dependencies on virtual env
In project folder, execute the following command:

```bash
pipenv install --dev
```

## Run
```bash
python grad.py
```
