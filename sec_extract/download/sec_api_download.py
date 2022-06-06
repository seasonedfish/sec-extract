import csv
import sys
from collections import namedtuple
from os import path

from sec_api import QueryApi, RenderApi

from sec_extract.keys import SEC_API_KEY

from requests.exceptions import ConnectionError

QUERY_API = QueryApi(SEC_API_KEY)
RENDER_API = RenderApi(SEC_API_KEY)


class FormNotFoundError(Exception):
    pass


Firm = namedtuple("Firm", ("ticker_symbol", "year", "cusip"))


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
        raise FormNotFoundError(f"No S-1 found for {ticker}")


def get_10k_url(ticker: str, year: int) -> str:
    year_range = f"[{year}-01-01T00:00:00 TO {year + 1}-01-01T00:00:00]"
    query = {
        "query": {
            "query_string": {
                "query": f"ticker:{ticker} AND formType:\"10-K\" AND filedAt: {year_range}",
                "time_zone": "America/New_York"
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
        raise FormNotFoundError(f"No 10-K found for {ticker} in range {year_range}")


def download_html(url: str, destination_path: str) -> None:
    if path.exists(destination_path):
        return

    try:
        html_string = RENDER_API.get_filing(url)
    except ConnectionError:
        print(f"Could not download {url}", file=sys.stderr)
        return

    with open(destination_path, "w") as f:
        f.write(html_string)


def main() -> None:
    firms = get_firms()
    for firm in firms:
        try:
            url_s1 = get_s1_url(firm.ticker_symbol)
        except FormNotFoundError as e:
            print(e, file=sys.stderr)
            continue
        download_html(url_s1, f"s1_html/{firm.ticker_symbol}.html")

    for firm in firms:
        try:
            url_10k = get_10k_url(firm.ticker_symbol, firm.year)
        except FormNotFoundError as e:
            print(e, file=sys.stderr)
            continue
        download_html(url_10k, f"10k_html/{firm.ticker_symbol}.html")


if __name__ == "__main__":
    main()
