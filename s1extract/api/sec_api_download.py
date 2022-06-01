import csv
import sys
from collections import namedtuple

from sec_api import QueryApi, RenderApi

from s1extract.api.keys import SEC_API_KEY

from requests.exceptions import ConnectionError

Firm = namedtuple("Firm", ("ticker_symbol", "year", "cusip"))

QUERY_API = QueryApi(SEC_API_KEY)
RENDER_API = RenderApi(SEC_API_KEY)


def get_firms() -> list[Firm]:
    with open("IPO Firm list 2005-2019.csv") as f:
        reader = csv.reader(f)
        reader.__next__()  # Skip first row
        firms = [Firm(*row) for row in reader]
    return firms


def get_s1_url(ticker: str) -> str:
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
    filings = QUERY_API.get_filings(query)
    try:
        return filings["filings"][0]["linkToFilingDetails"]
    except IndexError:
        raise ValueError(f"No S-1 found for {ticker}")


def download_s1_html(ticker: str) -> None:
    try:
        url = get_s1_url(ticker)
    except ValueError as e:
        print(e, file=sys.stderr)
        return

    try:
        html_string = RENDER_API.get_filing(url)
    except ConnectionError:
        print(f"Could not download html for {ticker}", file=sys.stderr)
        return

    with open(f"s1_html/{ticker}.html", "w") as f:
        f.write(html_string)


def main() -> None:
    firms = get_firms()
    start_index = firms.index(Firm("STVVY", "", "16938G107"))
    for firm in firms[start_index:]:
        download_s1_html(firm.ticker_symbol)


if __name__ == "__main__":
    main()
