import csv
from collections import namedtuple
from sec_api import QueryApi, RenderApi

from s1extract.api.keys import SEC_API_KEY

Firm = namedtuple("Firm", ("ticker_symbol", "year", "cusip"))

QUERY_API = QueryApi(SEC_API_KEY)
RENDER_API = RenderApi(SEC_API_KEY)


def get_firms():
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
    return filings["filings"][0]["linkToFilingDetails"]


def download_s1_html(ticker: str) -> None:
    url = get_s1_url(ticker)
    html_string = RENDER_API.get_filing(url)
    with open(f"s1_html/{ticker}.html", "w") as f:
        f.write(html_string)


def main():
    first_five_firms = get_firms()[0:5]
    print(first_five_firms)


if __name__ == "__main__":
    main()
