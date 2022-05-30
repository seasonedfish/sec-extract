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


def get_newest_s1(query_api: QueryApi, ticker: str):
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
    s1 = get_newest_s1(query_api, "ACHN")

    print(s1)


if __name__ == "__main__":
    main()
