import csv
from collections import namedtuple
from sec_api import QueryApi

from s1extract.api.keys import SEC_API_KEY

Firm = namedtuple("Firm", ("ticker_symbol", "year", "cusip"))


def get_firms():
    with open("IPO Firm list 2005-2019.csv") as f:
        reader = csv.reader(f)
        firms = tuple(
            Firm(*row)
            for row in reader[1:]
        )
    return firms


def main():
    query_api = QueryApi(api_key=SEC_API_KEY)
    query = {
        "query": {
            "query_string": {
                "query": "ticker:(AAOI) AND formType:\"S-1\""
            }
        },
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}]
    }
    filings = query_api.get_filings(query)

    print(filings)


if __name__ == "__main__":
    main()
