import csv
import sys
from pathlib import Path

from sec_api import QueryApi, RenderApi

from sec_extract.keys import SEC_API_KEY

from requests.exceptions import ConnectionError

QUERY_API = QueryApi(SEC_API_KEY)
RENDER_API = RenderApi(SEC_API_KEY)


def get_tickers() -> list[str]:
    with open("IPO Firm list 2005-2019.csv") as f:
        reader = csv.reader(f)
        reader.__next__()  # Skip first row
        firms = [row[0] for row in reader]  # Get only the ticker
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
    destination_path = Path(f"s1_html/{ticker}.html")
    if destination_path.exists():
        return

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

    with open(destination_path, "w") as f:
        f.write(html_string)


def main() -> None:
    tickers = get_tickers()
    for ticker in tickers:
        download_s1_html(ticker)


if __name__ == "__main__":
    main()
