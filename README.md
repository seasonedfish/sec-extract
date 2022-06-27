# SEC form data extraction

Repository for extracting data from S-1 and 10-K SEC forms.

## `sec-api`
This repository contains my fork of sec-api, which is licensed under the MIT license.
I have included its license [here](./sec_api/LICENSE.md).

The main difference between this and upstream is that
instead of throwing generic `Exceptions`, the library throws `APIErrors`.

## `download` package
This package contains the code for downloading the S-1 and 10-K forms.

## `extract` package
This package contains the code for extracting the business and management sections of the S-1 forms.