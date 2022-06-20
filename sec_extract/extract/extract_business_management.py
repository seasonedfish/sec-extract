from bs4 import BeautifulSoup


def extract_sections(soup: BeautifulSoup) -> str:
    return extract_section(soup, "BUSINESS") + extract_section(soup, "MANAGEMENT")


def get_anchor_names(soup: BeautifulSoup, section_name: str) -> (str, str):
    start_anchor = soup.find("a", text=section_name)
    end_anchor = start_anchor.find_next("a")
    return start_anchor.attrs["href"][1:], end_anchor.attrs["href"][1:]


def extract_between_tags(soup: BeautifulSoup, start_tag, end_tag) -> str:
    soup_string = str(soup)
    start_index = soup_string.index(str(start_tag))
    end_index = soup_string.index(str(end_tag))
    return soup_string[start_index: end_index]


def extract_section(soup: BeautifulSoup, section_name: str) -> str:
    start_anchor_name, end_anchor_name = get_anchor_names(soup, section_name)

    start_anchor = soup.find("a", attrs={"name": start_anchor_name})
    end_anchor = soup.find("a", attrs={"name": end_anchor_name})

    return extract_between_tags(soup, start_anchor, end_anchor)


def main():
    with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/download/s1_html/GMED.html") as f:
        soup = BeautifulSoup(f, "html.parser")

    result = extract_sections(soup)

    with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/extract/s1/GMED.html", "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
