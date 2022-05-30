import csv
from collections import namedtuple
from sec_api import QueryApi

from s1extract.api.keys import SEC_API_KEY
import requests

Firm = namedtuple("Firm", ("ticker_symbol", "year", "cusip"))


def get_firms():
    with open("IPO Firm list 2005-2019.csv") as f:
        reader = csv.reader(f)
        firms = tuple(
            Firm(*row)
            for row in reader[1:]
        )
    return firms


def get_s1_url(query_api: QueryApi, ticker: str):
    query = {
        "query": {
            "query_string": {
                "query": f"ticker:{ticker} AND formType:\"S-1\""
            }
        },
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}]
    }
    filings = query_api.get_filings(query)
    return filings["filings"][0]["linkToFilingDetails"]


def main():
    query_api = QueryApi(api_key=SEC_API_KEY)
    s1 = get_s1_url(query_api, "ACHN")

    r = requests.get(s1)
    with open("ACHN.htm", "wb") as f:
        f.write(r.content)

    print(s1)


if __name__ == "__main__":
    main()
