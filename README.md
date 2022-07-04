# SEC form data extraction

Repository for extracting data from S-1 and 10-K SEC forms.

## `sec-api`
This repository contains my fork of sec-api, which is licensed under the MIT license.
I have included its license [here](./sec_api/LICENSE.md).

The main difference between this and upstream is that
instead of throwing generic `Exceptions`, the library throws `APIErrors`.

## `download` package
This package contains the code for downloading the S-1 and 10-K forms.

To run:
1. Create the file `./sec_extract/keys.py` with the following code:
```python
SEC_API_KEY = "you-api-key"  # replace with your own API key

```
2. From the project root directory, run `python3 -m sec_extract.download`.
This creates a new directory, `./target`, which contains the downloaded forms.

## `extract` package
This package contains the code for extracting the business and management sections of the S-1 forms.

To run:
1. Run the `download` package, and make sure `./target/s1_html` contains the S-1 forms.
2. From the project root directory, run `python3 -m sec_extract.extract`.
The extracted sections will be in `./target`.