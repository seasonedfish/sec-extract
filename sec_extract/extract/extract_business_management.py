from bs4 import BeautifulSoup


def extract_sections(soup: BeautifulSoup) -> str:
    return extract_business_section(soup) + extract_management_section(soup)


def extract_between_tags(soup: BeautifulSoup, start_tag, end_tag) -> str:
    soup_string = str(soup)
    start_index = soup_string.index(str(start_tag))
    end_index = soup_string.index(str(end_tag))
    return soup_string[start_index: end_index]


def extract_business_section(soup: BeautifulSoup) -> str:
    start_anchor = soup.find("a", attrs={"name": "tx319036_10"})
    end_anchor = soup.find("a", attrs={"name": "tx319036_11"})

    return extract_between_tags(soup, start_anchor, end_anchor)


def extract_management_section(soup: BeautifulSoup) -> str:
    start_anchor = soup.find("a", attrs={"name": "tx319036_11"})
    end_anchor = soup.find("a", attrs={"name": "tx319036_12"})

    return extract_between_tags(soup, start_anchor, end_anchor)


def main():
    with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/download/s1_html/GMED.html") as f:
        soup = BeautifulSoup(f, "html.parser")

    result = extract_sections(soup)

    with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/extract/s1/GMED.html", "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
