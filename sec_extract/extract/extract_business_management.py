from bs4 import BeautifulSoup


def main():
    with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/download/s1_html/GMED.html") as f:
        soup = BeautifulSoup(f, "html.parser")

    business_anchor = soup.find("a", attrs={"name": "tx319036_10"})
    management_end_anchor = soup.find("a", attrs={"name": "tx319036_12"})

    soup_text = str(soup)
    start_index = soup_text.index(str(business_anchor))
    stop_index = soup_text.index(str(management_end_anchor))

    result = soup_text[start_index: stop_index]

    with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/extract/s1/GMED.html", "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
