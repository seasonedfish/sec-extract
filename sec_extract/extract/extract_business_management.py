import re

from bs4 import BeautifulSoup, Tag
import functools
import logging
import sys

BEFORE = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
"""

AFTER = """</body>
</html>
"""


class NoLinksFoundForAnySectionNameError(Exception):
    def __init__(self, section_names: list[str]):
        super().__init__(section_names)
        self.section_names = section_names

    def __str__(self):
        return f"No links found for any section name in {self.section_names}"


class MissingNamedAnchorError(Exception):
    def __init__(self, section_name: str):
        super().__init__(section_name)
        self.section_name = section_name

    def __str__(self):
        return f"Missing named anchor for \"{self.section_name}\""


class IncompatibleTableOfContentsError(Exception):
    pass


def is_start_anchor_for_section(tag, possible_section_names: list[str]) -> bool:
    try:
        if not (tag.name == "a" and "href" in tag.attrs):
            return False

        return any(
            # Regex removes duplicate whitespace
            # https://stackoverflow.com/a/1981366
            re.sub(r"\s\s+", " ", tag.text.lower().strip()) == s
            for s in possible_section_names
        )
    except AttributeError:
        return False


def is_start_anchor_for_different_section(tag, old_href) -> bool:
    try:
        if not (tag.name == "a" and "href" in tag.attrs):
            # Checks that it's a link
            return False

        if not (tag.text != "" and not tag.text.isdigit()):
            # Checks that it's not a page number or other invalid link
            return False

        if ("href", old_href) in tag.attrs.items():
            # Link points to the same place as old link.
            # This means that it's a table of contents with subsections,
            # which is unsupported.
            raise IncompatibleTableOfContentsError

        return True
    except AttributeError:
        return False


def get_anchor_names(soup: BeautifulSoup, possible_section_names: list[str]) -> (str, str):
    try:
        start_anchor = soup.find(
            functools.partial(is_start_anchor_for_section, possible_section_names=possible_section_names)
        )
        end_anchor = start_anchor.find_next(
            functools.partial(is_start_anchor_for_different_section, old_href=start_anchor.attrs["href"])
        )
    except AttributeError:
        raise NoLinksFoundForAnySectionNameError(possible_section_names)

    start_anchor_name = start_anchor.attrs["href"].replace("#", "")
    end_anchor_name = end_anchor.attrs["href"].replace("#", "")

    return start_anchor_name, end_anchor_name


def extract_between_tags(soup: BeautifulSoup, start_tag, end_tag) -> str:
    soup_string = str(soup)
    start_index = soup_string.index(str(start_tag))
    end_index = soup_string.index(str(end_tag))
    return soup_string[start_index: end_index]


def find_parent_with_siblings(tag) -> Tag:
    if any(isinstance(sibling, Tag) for sibling in tag.next_siblings):
        return tag
    else:
        return find_parent_with_siblings(tag.parent)


def extract_section(soup: BeautifulSoup, possible_section_names: list[str]) -> str:
    start_anchor_name, end_anchor_name = get_anchor_names(soup, possible_section_names)

    start_anchor = soup.find("a", attrs={"name": start_anchor_name})
    end_anchor = soup.find("a", attrs={"name": end_anchor_name})

    if start_anchor is None:
        raise MissingNamedAnchorError(start_anchor_name)
    if end_anchor is None:
        raise MissingNamedAnchorError(end_anchor_name)

    return extract_between_tags(
        soup,
        find_parent_with_siblings(start_anchor),
        find_parent_with_siblings(end_anchor)
    )


def extract_section_and_save(soup: BeautifulSoup, ticker: str, possible_section_names: list[str]) -> bool:
    try:
        section = extract_section(soup, possible_section_names)
    except NoLinksFoundForAnySectionNameError as e:
        logging.warning(f"{e} for {ticker}")
        return False
    except MissingNamedAnchorError as e:
        logging.warning(f"{e} for {ticker}")
        return False
    except IncompatibleTableOfContentsError:
        logging.warning(f"Incompatible table of contents for {ticker}")
        return False

    with open(f"s1_{possible_section_names[0]}/{ticker}.html", "w") as f:
        f.write(BEFORE)
        f.write(section)
        f.write(AFTER)
    return True


def main():
    tickers = [
        "DBTK", "SUN", "KRYS", "QMAR", "PLSE", "PFPT", "TRVN", "CIVI", "TXTR", "HUBS"
    ]
    logging.basicConfig(level="DEBUG")
    sys.setrecursionlimit(10000)  # Required to cast soup objects to strings
    for ticker in tickers:
        logging.info(f"Now extracting {ticker}")
        with open(f"../download/s1_html/{ticker}.html") as f:
            soup = BeautifulSoup(f, "html.parser")

        extract_section_and_save(soup, ticker, ["business", "what we do", "proposed business", "our business"])
        extract_section_and_save(soup, ticker, ["management"])


if __name__ == "__main__":
    main()
