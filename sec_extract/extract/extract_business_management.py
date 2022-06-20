from bs4 import BeautifulSoup, Tag

with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/download/s1_html/GMED.html") as f:
    soup = BeautifulSoup(f, "html.parser")

business_anchor = soup.find("a", attrs={"name": "tx319036_10"})

business_section = []
for element in business_anchor.next_elements:
    if element.name == "a" and ("name", "tx319036_11") in element.attrs.items():
        break
    else:
        business_section.append(str(element))

with open("/Users/fisher/PycharmProjects/sec-extract/sec_extract/extract/s1/GMED.html", "w") as f:
    f.writelines(business_section)
