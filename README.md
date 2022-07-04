# SEC form data extraction

Repository for extracting data from S-1 and 10-K SEC forms.

## Setup
1. Clone or download the repo.
2. In the project's root directory, install the dependencies.
```bash
# Use this if you use Poetry
poetry install
poetry shell
# Use this is you pip
python3 -m venv .venv
source ./venv/bin/activate
python3 -m pip install .
```
3. Create the file `./sec_extract/keys.py`, replacing `your-api-key` with your sec-api key.
```python
SEC_API_KEY = "your-api-key"
```

## `sec-api`
This repository contains my fork of sec-api, which is licensed under the MIT license.
I have included its license [here](./sec_api/LICENSE.md).

The main difference between this and upstream is that
instead of throwing generic `Exceptions`, the library throws `APIErrors`.

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