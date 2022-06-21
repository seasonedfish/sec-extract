from bs4 import BeautifulSoup
import functools


def extract_sections(soup: BeautifulSoup) -> str:
    return extract_section(soup, "business") + extract_section(soup, "management")


def is_start_anchor_for_section(tag, section_name: str) -> bool:
    return tag.name.lower() == "a" and tag.text.lower() == section_name


def is_start_anchor(tag) -> bool:
    return (
        tag.name.lower() == "a"
        and tag.text != ""
        and not tag.text.isdigit()
    )


def get_anchor_names(soup: BeautifulSoup, section_name: str) -> (str, str):
    start_anchor = soup.find(
        functools.partial(is_start_anchor_for_section, section_name=section_name)
    )
    end_anchor = start_anchor.find_next(is_start_anchor)

    start_anchor_name = start_anchor.attrs["href"].replace("#", "")
    end_anchor_name = end_anchor.attrs["href"].replace("#", "")

    return start_anchor_name, end_anchor_name


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
    ticker = "MULE"
    with open(f"/Users/fisher/PycharmProjects/sec-extract/sec_extract/download/s1_html/{ticker}.html") as f:
        soup = BeautifulSoup(f, "html.parser")

    business = extract_section(soup, "business")
    management = extract_section(soup, "management")

    with open(f"/Users/fisher/PycharmProjects/sec-extract/sec_extract/extract/s1_business/{ticker}.html", "w") as f:
        f.write(business)
    with open(f"/Users/fisher/PycharmProjects/sec-extract/sec_extract/extract/s1_management/{ticker}.html", "w") as f:
        f.write(management)


if __name__ == "__main__":
    main()
