# SEC form data extraction

Repository for extracting data from S-1 and 10-K SEC forms.

## Setup
1. Clone or download the repo.
2. In the project's root directory, install the dependencies.
```bash
# Use this if you use Poetry
poetry install
poetry shell
```
```bash
# Use this is you use pip
python3 -m venv .venv
source ./venv/bin/activate
python3 -m pip install .
```
3. Create the file `./sec_extract/keys.py`, replacing `your-api-key` with your sec-api key.
```python
SEC_API_KEY = "your-api-key"
```

## `download` package
This package contains the code for downloading the S-1 and 10-K forms.

To run:
1. From the project root directory, run `python3 -m sec_extract.download`.
This creates a new directory, `./target`, which contains the downloaded forms.

## `extract` package
This package contains the code for extracting the business and management sections of the S-1 forms.

To run (only run after running `download` first):
1. From the project root directory, run `python3 -m sec_extract.extract`.
The extracted sections will be in `./target`.