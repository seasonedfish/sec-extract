import csv
import logging
from collections import namedtuple
from os import path
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from sec_api import QueryApi, RenderApi
from sec_extract.keys import SEC_API_KEY

QUERY_API = QueryApi(SEC_API_KEY)
RENDER_API = RenderApi(SEC_API_KEY)

THREADS = 8


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
        "sort": [{"filedAt": {"order": "asc"}}]
    }
    filings = QUERY_API.get_filings(query)
    try:
        return filings["filings"][0]["linkToFilingDetails"].replace("ix?doc=/", "")
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
        return filings["filings"][0]["linkToFilingDetails"].replace("ix?doc=/", "")
    except IndexError:
        raise FormNotFoundError(f"No 10-K found for {ticker} in range {year_range}")


def download_html(url: str, destination_path: str) -> None:
    html_string = RENDER_API.get_filing(url)

    with open(destination_path, "w") as f:
        f.write(html_string)
    logging.info(f"Downloaded {destination_path}")


def get_s1(ticker: str) -> str:
    logging.info(f"Fetching S-1 for {ticker}")
    return RENDER_API.get_filing(get_s1_url(ticker))


def save_to_file(s: str, destination_path: str) -> None:
    with open(destination_path, "w") as f:
        f.write(s)
    logging.info(f"Saved {destination_path}")


def download_all_s1s(firms: list[Firm]) -> None:
    with ThreadPoolExecutor(THREADS) as executor:
        futures = [
            executor.submit(get_s1, firm.ticker_symbol)
            for firm in firms
        ]

        for firm, future in zip(firms, futures):
            if future.exception():
                logging.warning(future.exception())
                continue

            save_to_file(
                future.result(),
                f"s1_html/{firm.ticker_symbol}.html"
            )


def download_all_10ks(firms: list[Firm]) -> None:
    for firm in firms:
        if firm.year == "":
            logging.warning(f"No year found for {firm}")
            continue

        for i in range(3, 6):
            document_year = int(firm.year) + i
            destination_path = f"10k_html/{firm.ticker_symbol}{document_year}.html"
            if path.exists(destination_path):
                continue

            try:
                url_10k = get_10k_url(firm.ticker_symbol, document_year)
            except FormNotFoundError as e:
                logging.warning(e)
                continue
            except ConnectionError as e:
                logging.warning(e)
                continue
            download_html(url_10k, destination_path)


def main() -> None:
    logging.basicConfig(level="INFO")
    firms = get_firms()

    download_all_s1s(firms)


if __name__ == "__main__":
    main()
